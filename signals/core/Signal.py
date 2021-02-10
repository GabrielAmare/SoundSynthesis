from functools import reduce
from operator import mul

from .utils import MathUtils
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

    def __add__(self, other):
        return SignalSum(self, other)

    def __iadd__(self, other):
        return SignalSum(self, other)

    def __mul__(self, other):
        return SignalProd(self, other)

    def __imul__(self, other):
        return SignalProd(self, other)

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


class SignalProd(Signal):
    @classmethod
    def parse_signals(cls, *signals):
        final = []
        for signal in signals:
            if isinstance(signal, SignalProd):
                final.extend(cls.parse_signals(*signal.signals))
            else:
                final.append(signal)
        return final

    def __init__(self, *signals):
        assert all(isinstance(signal, Signal) for signal in signals)
        self.signals = SignalProd.parse_signals(*signals)

    def __repr__(self):
        return " * ".join(map(repr, self.signals))

    def __call__(self, t):
        if self.signals:
            return reduce(mul, (signal(t) for signal in self.signals))
        else:
            return 0

    def i_sample_data(self, time_sample):
        samples = (signal.i_sample_data(time_sample) for signal in self.signals)
        for values in zip(*samples):
            if values:
                yield reduce(mul, values)
            else:
                yield 0


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

    def i_sample_data(self, time_sample):
        samples = (signal.i_sample_data(time_sample) for signal in self.signals)
        for values in zip(*samples):
            if values:
                yield sum(values)
            else:
                yield 0
