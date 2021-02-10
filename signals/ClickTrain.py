from .core import SimpleSignal
from math import tau

__authors__ = ["Elie Grinfeder", "Gabriel Amare"]


class ClickTrain(SimpleSignal):
    def __init__(self, frequency, duration, amplitude: float = 1.0, phase: float = 0.0):
        """
            :param frequency: expressed in Hz
            :param duration: duration of the click expressed in s
            :param amplitude: expressed without unit
            :param phase: expressed in radians
        """
        super().__init__(frequency)
        assert amplitude != 0,\
            f"The amplitude of the click train signal shall not be 0"
        assert 0 < duration < self.period,\
            f"The duration of a click shall not exceed the period of the click train signal"
        self.amplitude = amplitude
        self.phase = phase
        self.duration = duration

    def __call__(self, t):
        return self.amplitude if 0 <= (t - self.phase / tau) % self.period < self.duration else 0

    def __repr__(self):
        amplitude = self.amplitude
        duration = self.duration
        period = self.period
        phase = self.phase / tau

        if amplitude % 1 == 0:
            amplitude = int(amplitude)
        if period % 1 == 0:
            period = int(period)
        if phase % 1 == 0:
            phase = int(phase)
        if duration % 1 == 0:
            duration = int(duration)

        return (f"{amplitude} * " if amplitude != 1 else "") + "(0 <= " + \
               (f"(t - {phase})" if phase > 0 else f"(t + {-phase})" if phase < 0 else "t") + f"% {period} < {duration})"
