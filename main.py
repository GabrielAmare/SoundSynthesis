from signals import *
import math

if __name__ == '__main__':
    hs = HarmonicSerie(
        base_frequency=220.0,
        number_of_harmonics=10,
        harmonics_amplitude_function=lambda n: 0.1 / n ** 2
    )

    E1 = lambda n: lambda t: ((n * t) / 2) ** 2 * math.exp(2 - n * t)

    signal = Envelop(
        original_signal=hs + WhiteNoise(amplitude=0.001),
        amplitude_function=E1(5)
    )

    t_min, t_max = (0, 5)

    signal.plot(t_min=t_min, t_max=t_max)

    signal.play(duration=t_max - t_min, t_offset=t_min)
