from math import sin, pi
from .core import SimpleSignal


class Sine(SimpleSignal):
    def __init__(self, frequency, amplitude=1.0, phase=0.0):
        """
            Create a sine wave of the form :   S(t) = A * sin(2 pi f t + p)   [where A = amplitude, f = frequency, p = phase, t = time]
        :param frequency: The frequency of the sine
        :param amplitude: The amplitude of the sine
        :param phase: The phase of the sine
        """
        super().__init__(frequency)
        self.amplitude = amplitude  # m
        self.phase = phase  # m (if the phase is a function, it will be called on t when self is called)

    def __call__(self, t):
        """
            See Signal.__call__ docstring
            >>> help(Signal.__init__)
        """
        return self.amplitude * sin(2 * pi * self.frequency * t + self.phase)

    def __repr__(self):
        """Displays the sine equation"""
        result = ""

        amplitude = round(self.amplitude, 3)
        frequency = round(self.frequency, 3)
        phase = round(self.phase, 3)

        if amplitude != 1:
            result += f"{amplitude}*"

        if frequency != 1:
            result += f"sin(2*π*{frequency}*t"
        else:
            result += f"sin(2*π*t"

        if isinstance(phase, (int, float)):
            if phase > 0:
                result += f" + {phase})"
            elif phase < 0:
                result += f" - {phase})"
        else:
            result += f" + {phase}"

        result += ")"

        return result
