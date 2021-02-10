from functools import reduce
from operator import mul
from .Signal import Signal


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
