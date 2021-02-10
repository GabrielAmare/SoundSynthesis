from .TimeSample import TimeSample
from .SignalSample import SignalSample


class Signal:
    def __call__(self, t):
        """
            For a given time (in seconds) return the corresponding height of the signal
        :param t: The time (in seconds)
        :return: The intensity of the signal at that time
        """
        raise NotImplementedError

    def i_sample_data(self, time_sample):
        for t in time_sample:
            yield self(t)

    def sample_data(self, time_sample):
        return tuple(self.i_sample_data(time_sample))

    def sample(self,
               duration: float = None,
               t_max: float = None, n_frames: int = None,
               t_min: float = 0, frame_rate: float = 44100.0):
        time_sample = TimeSample(duration=duration, t_min=t_min, t_max=t_max, n_frames=n_frames, frame_rate=frame_rate)
        return SignalSample.from_signal(
            time_sample=time_sample,
            signal=self
        )

    def to_wave(self,
                filepath: str,
                duration: float = None,
                t_max: float = None, n_frames: int = None,
                t_min: float = 0, frame_rate: float = 44100.0,
                norm_to=None, sampwidth=2, bufsize=2048):
        """Sample methods made accessible from the signal directly (see the corresponding method definition in the SignalSample class)"""
        self.sample(duration=duration, t_min=t_min, t_max=t_max, n_frames=n_frames, frame_rate=frame_rate) \
            .to_wave(filepath=filepath, norm_to=norm_to, sampwidth=sampwidth, bufsize=bufsize)

    def play(self,
             duration: float = None,
             t_max: float = None, n_frames: int = None,
             t_min: float = 0, frame_rate: float = 44100.0,
             norm_to=None, sampwidth=2, bufsize=2048):
        """Sample methods made accessible from the signal directly (see the corresponding method definition in the SignalSample class)"""
        self.sample(duration=duration, t_min=t_min, t_max=t_max, n_frames=n_frames, frame_rate=frame_rate) \
            .play(norm_to=norm_to, sampwidth=sampwidth, bufsize=bufsize)

    def plot(self,
             duration: float = None,
             t_max: float = None, n_frames: int = None,
             t_min: float = 0, frame_rate: float = 44100.0,
             title: str = "", xlabel: str = "", ylabel: str = "", export_to: str = None):
        """Sample methods made accessible from the signal directly (see the corresponding method definition in the SignalSample class)"""
        self.sample(duration=duration, t_min=t_min, t_max=t_max, n_frames=n_frames, frame_rate=frame_rate) \
            .plot(xlabel=xlabel, ylabel=ylabel, title=title, export_to=export_to)

    __add__ = None
    __mul__ = None


class PeriodicSignal(Signal):
    period: float


class SimpleSignal(PeriodicSignal):
    """
        Simple signals are signals which have a frequency param (from which their period can be deduced)
    """

    def __init__(self, frequency: float):
        assert frequency != 0, "SimpleSignal.__init__, frequency shall not be 0"
        self.frequency = frequency

        self.period = 1 / self.frequency
