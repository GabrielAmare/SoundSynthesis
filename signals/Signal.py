import itertools
import struct
import wave

import playsound  # to install
import matplotlib.pyplot as plt


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


class Signal:
    temp_wave_filepath = "temp.wav"

    def __call__(self, t):
        """
            For a given time (in seconds) return the corresponding height of the signal
        :param t: The time (in seconds)
        :return: The intensity of the signal at that time
        """
        raise NotImplementedError

    def sample(self, frame_rate: float, n_frames: int, t_offset: float = 0.0, offset: float = 0.0):
        """
        Return a sample of the signal
        :param frame_rate: the rate of frames per second
        :param n_frames: the number of frames wanted for the sample
        :param offset: the offset (between 0 and 1) (if you don't know, don't touch, even if it shoudn't change anything in practice)
        :return: the desired sample of the signal, in the form of a list of floats
        """
        assert 0 <= offset <= 1

        for i_frame in range(n_frames):
            yield self(t_offset + (i_frame + offset) / frame_rate)

    def sample_enum(self, frame_rate: float, n_frames: int, t_offset: float = 0.0, offset: float = 0.0):
        """
        Return a sample of the coordinates (t, signal(t))
        -> see the Signal.sample method for details on the params
        :return: the desired coordinates sample
        """
        assert 0 <= offset <= 1
        for i_frame, y in enumerate(self.sample(frame_rate, n_frames, t_offset=t_offset)):
            yield t_offset + i_frame / frame_rate, y

    def to_wave(self, filename, n_frames=None, duration=None, frame_rate=44100, sampwidth=2, bufsize=2048, **config):
        """
            Allow to create a wave file from the signal (given the sample params and the wave params)
        :param filename: The name of the file to save
        :param n_frames: see Signal.sample method docstring
        :param frame_rate: see Signal.sample method docstring
        :param duration: you can provide duration instead of n_frames OR frame_rate (the calculation for the missing param will be done automatically)
        :param sampwidth: The sample width (number of bytes for the amplitude)
        :param bufsize: The size of the buffer used to write the wave file (used to reduce memory consumption and improve performances)
        :return: None (to access the file use it's filename
        """
        if n_frames is None and duration is not None and frame_rate is not None:
            n_frames = int(duration * frame_rate)
        elif n_frames is not None and duration is None and frame_rate is not None:
            duration = n_frames * frame_rate
        elif n_frames is not None and duration is not None and frame_rate is None:
            frame_rate = duration / n_frames
        else:
            raise Exception(
                f"{self.__class__.__name__}.to_wave(...) : You have to specify two parameters of ('n_frames', 'duration', 'frame_rate')")

        assert n_frames % 1 == 0

        n_frames = int(n_frames)
        frame_rate = float(frame_rate)

        nchannels = 2

        sample = self.sample(frame_rate=frame_rate, n_frames=n_frames, **config)

        samples = [sample]

        with wave.open(filename, 'w') as file:
            file.setparams((nchannels, sampwidth, frame_rate, n_frames, 'NONE', 'not compressed'))

            bin_size = 2 ** (sampwidth * 8)

            max_amplitude = float(int(bin_size / 2) - 1)

            for chunk in grouper(bufsize, samples):
                frames = b''.join(
                    b''.join(
                        struct.pack('h', int(max_amplitude * sample)) for sample in channels
                    ) for channels in chunk if channels is not None
                )
                file.writeframesraw(frames)

    def play(self, duration, **config):
        """
            Play the sound for a given duration (save a temporary file, play it)
        :param duration: Duration in seconds
        :return: None
        """
        filepath = self.__class__.temp_wave_filepath

        self.to_wave(filepath, duration=duration, **config)

        playsound.playsound(filepath)

        # TODO : os.remove(filepath) doesn't work properly here.
        #  I guess it's because playsound doesn't close the filestream of something like that.
        #  The temp.wav file shouldn't remain after the program lifetime.

    def __add__(self, other):
        return SignalSum(self, other)

    def plot(self, t_min: float, t_max: float, frame_rate: float = 44100.0,
             title: str = "", xlabel: str = "", ylabel: str = ""):
        P = self.sample_enum(
            frame_rate=frame_rate,
            n_frames=int((t_max - t_min) * frame_rate),
            t_offset=t_min
        )

        X, Y = map(list, zip(*P))

        fig, ax = plt.subplots()
        ax.plot(X, Y)

        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        ax.grid()

        # fig.savefig("test.png")
        plt.show()


class SignalSum(Signal):
    def __init__(self, *signals):
        assert all(isinstance(signal, Signal) for signal in signals)
        self.signals = list(signals)

    def __repr__(self):
        return " + ".join(map(repr, self.signals))

    def __call__(self, t):
        if self.signals:
            return sum(signal(t) for signal in self.signals)
        else:
            return 0
