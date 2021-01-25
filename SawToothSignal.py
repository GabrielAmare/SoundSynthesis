"""
    Example of package external implementation of a custom signal (in that case a PeriodicSignal) with the 'saw tooth signal'
"""
from signals import SimpleSignal


class SawToothSignal(SimpleSignal):
    def __init__(self, frequency: float, amplitude: float, phase: float = 0.0, revert: bool = False):
        super().__init__(frequency)
        self.amplitude = amplitude
        self.phase = phase
        self.revert = revert

    def __call__(self, t):
        base = ((t - self.phase) * self.frequency) % 1
        if self.revert:
            return self.amplitude * (1 - base)
        else:
            return self.amplitude * base
