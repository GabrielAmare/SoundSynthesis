from .core import Signal

__authors__ = ["Elie Grinfeder", "Gabriel Amare"]


class Click(Signal):
    def __init__(self, duration, amplitude: float = 1.0, phase: float = 1.0):
        assert duration > 0
        self.duration = duration
        self.amplitude = abs(amplitude)
        self.phase = phase

    def __call__(self, t):
        return self.amplitude if 0 <= t - self.phase < self.duration else 0

    def __repr__(self):
        return f"{self.amplitude} * ({self.phase} <= t < {self.phase + self.duration})"
