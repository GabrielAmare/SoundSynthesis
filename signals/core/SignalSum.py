from functools import reduce
from operator import add
from .Signal import Signal, PeriodicSignal
from .utils import MathUtils


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
            return reduce(add, (signal(t) for signal in self.signals))
        else:
            return 0

    def i_sample_data(self, time_sample):
        samples = (signal.i_sample_data(time_sample) for signal in self.signals)
        for values in zip(*samples):
            if values:
                yield sum(values)
            else:
                yield 0
