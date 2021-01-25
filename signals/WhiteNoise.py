from math import fabs as abs
from random import uniform
from .core import Signal


class WhiteNoise(Signal):
    def __init__(self, amplitude: float):
        """
            Create white noise for a random uniform distribution law between [-amplitude, +amplitude]
        :param amplitude: The maximum amplitude of the signal
        """
        self.amplitude = abs(amplitude)

    @property
    def period(self):
        return 0

    def __call__(self, t):
        """
            See Signal.__call__ docstring
            >>> help(Signal.__init__)
        """
        return self.amplitude * uniform(-1, 1)

    def __repr__(self):
        """Displays the white noise equation (where U is used as an abbreviation for random uniform distribution)"""
        return f"{self.amplitude} * Uniform(-1, 1)"
