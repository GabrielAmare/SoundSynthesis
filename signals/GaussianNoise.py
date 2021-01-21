from .Signal import Signal
from random import gauss


class GaussianNoise(Signal):
    def __init__(self, amplitude, mu, sigma):
        self.amplitude = amplitude
        self.mu = mu
        self.sigma = sigma

    def __call__(self, t):
        return self.amplitude * gauss(self.mu, self.sigma)

    def __repr__(self):
        return f"{self.amplitude} * Gauss({self.mu}, {self.sigma})"
