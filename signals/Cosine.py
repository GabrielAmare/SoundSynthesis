from math import cos, tau
from .core import SimpleSignal


class Cosine(SimpleSignal):
    def __init__(self, frequency, amplitude=1.0, phase=0.0):
        """
            Create a cosine wave of the form :   S(t) = A * cos(2 pi f t + p)   [where A = amplitude, f = frequency, p = phase, t = time]
        :param frequency: The frequency of the cosine
        :param amplitude: The amplitude of the cosine
        :param phase: The phase of the cosine
        """
        super().__init__(frequency)
        self.amplitude = amplitude
        self.phase = phase

    def __call__(self, t):
        """
            See Signal.__call__ docstring
            >>> help(Signal.__init__)
        """
        return self.amplitude * cos(tau * self.frequency * t + self.phase)

    def __repr__(self):
        """Displays the cosine equation"""
        result = ""

        amplitude = round(self.amplitude, 3)
        frequency = round(self.frequency, 3)
        phase = round(self.phase, 3)

        if amplitude != 1:
            result += f"{amplitude}*"

        if frequency != 1:
            result += f"cos(2*π*{frequency}*t"
        else:
            result += f"cos(2*π*t"

        if isinstance(phase, (int, float)):
            if phase > 0:
                result += f" + {phase})"
            elif phase < 0:
                result += f" - {phase})"
        else:
            result += f" + {phase}"

        result += ")"

        return result
