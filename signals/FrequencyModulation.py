from signals.core import Signal
from signals.Sine import Sine
from math import sin, tau

__author__ = "Elie Grinfeder"
__version__ = "1.0"


class FrequencyModulation(Signal):
    def __init__(self, carrier: Sine, carried: Signal, depth: float = 1):
        """
            Create a frequency modulated signal
            :param carrier: carrier wave
            :param carried: carried wave
            :param depth: modulation factor
        """
        self.carrier = carrier  # xp = Ap sin(wp * t)
        self.carried = carried  # xm = Am sin(wm * t)
        self.depth = depth

    def __call__(self, t):
        amplitude = self.carrier.amplitude
        frequency = self.carrier.frequency + self.depth * self.carried(t)
        phase = self.carrier.phase
        return amplitude * sin(tau * frequency * t + phase)
