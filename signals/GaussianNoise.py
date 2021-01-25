from random import gauss
from .core import Signal


class GaussianNoise(Signal):
    def __init__(self, amplitude, mu, sigma):
        self.amplitude = amplitude
        self.mu = mu
        self.sigma = sigma

    @property
    def period(self):
        return 0

    def __call__(self, t):
        return self.amplitude * gauss(self.mu, self.sigma)

    def __repr__(self):
        return f"{self.amplitude} * Gauss({self.mu}, {self.sigma})"
