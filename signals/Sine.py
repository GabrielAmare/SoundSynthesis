from math import sin, tau
from .core import SimpleSignal
from .core.utils import trig


class Sine(SimpleSignal):
    def __init__(self, frequency, amplitude=1.0, phase=0.0):
        """
            Create a sine wave of the form :   S(t) = A * sin(2 pi f t + p)   [where A = amplitude, f = frequency, p = phase, t = time]
        :param frequency: The frequency of the sine
        :param amplitude: The amplitude of the sine
        :param phase: The phase of the sine
        """
        super().__init__(frequency)
        self.amplitude = amplitude
        self.phase = phase

    def __call__(self, t):
        return self.amplitude * sin(tau * self.frequency * t + self.phase)

    def __repr__(self):
        """Displays the sine equation"""
        result = ""

        amplitude = round(self.amplitude, 3)
        frequency = tau * self.frequency
        phase = round(self.phase, 3)

        if amplitude != 1:
            result += f"{amplitude}*"

        if frequency != 1:
            result += f"sin({frequency}*t"
        else:
            result += f"sin(t"

        if isinstance(phase, (int, float)):
            if phase > 0:
                result += f" + {phase})"
            elif phase < 0:
                result += f" - {-phase})"
        else:
            result += f" + {phase}"

        result += ")"

        return result

    def i_sample_data(self, time_sample):
        """This code is ugly but works 50% faster than the classic i_sample_data"""
        c0, s0 = trig(self.frequency, time_sample.t_min, self.amplitude, self.phase)

        dc1, ds1 = trig(self.frequency, 1 * time_sample.frame_width)
        dc2, ds2 = trig(self.frequency, 2 * time_sample.frame_width)
        dc3, ds3 = trig(self.frequency, 3 * time_sample.frame_width)
        dc4, ds4 = trig(self.frequency, 4 * time_sample.frame_width)
        dc5, ds5 = trig(self.frequency, 5 * time_sample.frame_width)
        dc6, ds6 = trig(self.frequency, 6 * time_sample.frame_width)
        dc7, ds7 = trig(self.frequency, 7 * time_sample.frame_width)
        dc8, ds8 = trig(self.frequency, 8 * time_sample.frame_width)
        dc9, ds9 = trig(self.frequency, 9 * time_sample.frame_width)
        dc10, ds10 = trig(self.frequency, 10 * time_sample.frame_width)

        n = time_sample.n_frames

        while 0 <= n:
            yield s0
            if n <= 1:
                return
            yield c0 * ds1 + s0 * dc1
            if n <= 2:
                return
            yield c0 * ds2 + s0 * dc2
            if n <= 3:
                return
            yield c0 * ds3 + s0 * dc3
            if n <= 4:
                return
            yield c0 * ds4 + s0 * dc4
            if n <= 5:
                return
            yield c0 * ds5 + s0 * dc5
            if n <= 6:
                return
            yield c0 * ds6 + s0 * dc6
            if n <= 7:
                return
            yield c0 * ds7 + s0 * dc7
            if n <= 8:
                return
            yield c0 * ds8 + s0 * dc8
            if n <= 9:
                return
            yield c0 * ds9 + s0 * dc9
            c0, s0 = c0 * dc10 - s0 * ds10, c0 * ds10 + s0 * dc10

            n -= 10
