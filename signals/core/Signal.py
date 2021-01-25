import struct
import wave
import playsound  # to install
import matplotlib.pyplot as plt

from .utils import MathUtils, grouper
from .TimeSample import TimeSample


class Sample:
    temp_wave_filepath = "temp.wav"

    @classmethod
    def from_signal(cls, time_sample, signal):
        return cls(time_sample=time_sample, Y=[signal(t) for t in time_sample])

    def __init__(self, time_sample: TimeSample, Y):
        assert len(time_sample) == len(Y)
        self.time_sample = time_sample
        self.Y = Y

    def plot(self, title: str = "", xlabel: str = "", ylabel: str = "", export_to: str = None):
        """
            :param title: the plot title
            :param xlabel: the label for the x axis (time axis)
            :param ylabel: the label for the y axis (amplitude axis)

            :param export_to: if you want to export the plot as an image, give it the desired filepath for the image
        """

        fig, ax = plt.subplots()
        ax.plot(list(self.time_sample), self.Y)

        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        ax.grid()
        if export_to:
            fig.savefig(export_to)
        plt.show()

    def to_wave(self, filepath, norm_to=None, sampwidth=2, bufsize=2048):
        nchannels = 2

        data = self.Y

        if norm_to is not None:
            data = list(data)
            amplitude_max = max(map(abs, data))
            data = ((norm_to * amplitude) / amplitude_max for amplitude in data)

        samples = [data]

        with wave.open(filepath, 'w') as file:
            file.setparams((nchannels, sampwidth, self.time_sample.frame_rate, self.time_sample.n_frames, 'NONE',
                            'not compressed'))

            bin_size = 2 ** (sampwidth * 8)

            max_amplitude = float(int(bin_size / 2) - 1)

            for chunk in grouper(bufsize, samples):
                frames = b''.join(
                    b''.join(
                        struct.pack('h', int(max_amplitude * sample)) for sample in channels
                    ) for channels in chunk if channels is not None
                )
                file.writeframesraw(frames)

    def play(self, **config):
        filepath = self.__class__.temp_wave_filepath

        self.to_wave(filepath, **config)

        playsound.playsound(filepath)

        # TODO : os.remove(filepath) doesn't work properly here.
        #  I guess it's because playsound doesn't close the filestream of something like that.
        #  The temp.wav file shouldn't remain after the program lifetime.


class Signal:
    def __call__(self, t):
        """
            For a given time (in seconds) return the corresponding height of the signal
        :param t: The time (in seconds)
        :return: The intensity of the signal at that time
        """
        raise NotImplementedError

    def __add__(self, other):
        return SignalSum(self, other)

    def __iadd__(self, other):
        return SignalSum(self, other)

    def sample(self, t_min: float = None, t_max: float = None, duration: float = None, n_frames: int = None,
               frame_rate: float = 44100.0):
        time_sample = TimeSample(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)
        return Sample.from_signal(
            time_sample=time_sample,
            signal=self
        )

    def to_wave(self,
                filepath: str,
                t_min: float = None, t_max: float = None, duration: float = None, n_frames: int = None,
                frame_rate: float = 44100.0,
                norm_to=None, sampwidth=2, bufsize=2048):
        self.sample(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate) \
            .to_wave(filepath=filepath, norm_to=norm_to, sampwidth=sampwidth, bufsize=bufsize)

    def play(self,
             t_min: float = None, t_max: float = None, duration: float = None, n_frames: int = None,
             frame_rate: float = 44100.0,
             norm_to=None, sampwidth=2, bufsize=2048):
        self.sample(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate) \
            .play(norm_to=norm_to, sampwidth=sampwidth, bufsize=bufsize)

    def plot(self,
             t_min: float = None, t_max: float = None, duration: float = None, n_frames: int = None,
             frame_rate: float = 44100.0,
             title: str = "", xlabel: str = "", ylabel: str = "", export_to: str = None):
        self.sample(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate) \
            .plot(xlabel=xlabel, ylabel=ylabel, title=title, export_to=export_to)


class PeriodicSignal(Signal):
    period: float


class SimpleSignal(PeriodicSignal):
    def __init__(self, frequency: float):
        assert frequency != 0, "FrequencySignal.__init__, frequency shall not be 0"
        self.frequency = frequency

        self.period = 1 / self.frequency


class SignalSum(Signal):
    @classmethod
    def parse_signals(cls, *signals):
        final = []
        for signal in signals:
            if isinstance(signal, SignalSum):
                final.extend(cls.parse_signals(*signal.signals))
            else:
                final.append(signal)
        return final

    def __init__(self, *signals):
        assert all(isinstance(signal, Signal) for signal in signals)
        self.signals = SignalSum.parse_signals(*signals)

    @property
    def period(self):
        """Can be calculated only if all of it's compounds are periodic"""
        assert all(isinstance(signal, PeriodicSignal) for signal in self.signals), \
            "SignalSum.period exists only when all the compounds are periodic ! "
        periods = [signal.period for signal in self.signals]
        if 0 in periods:
            return 0
        else:
            return MathUtils.ppcm(*periods)

    def __repr__(self):
        return " + ".join(map(repr, self.signals))

    def __call__(self, t):
        if self.signals:
            return sum(signal(t) for signal in self.signals)
        else:
            return 0
