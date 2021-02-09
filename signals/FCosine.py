from math import cos, tau
from typing import Union

from .core.Signal import Signal


class FCosine(Signal):
    """
        Make the same thing as Cosine but the frequency, amplitude and phase can be functions of time
    """
    allowed = Union[int, float, callable, Signal]

    def __init__(self, frequency: allowed, amplitude: allowed = 1.0, phase: allowed = 0.0):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase

    def __call__(self, t):
        frequency = self.frequency(t) if hasattr(self.frequency, '__call__') else self.frequency
        amplitude = self.amplitude(t) if hasattr(self.amplitude, '__call__') else self.amplitude
        phase = self.phase(t) if hasattr(self.phase, '__call__') else self.phase
        return amplitude * cos(tau * frequency * t + phase)
