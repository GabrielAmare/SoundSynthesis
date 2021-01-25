from signals import *
import math

if __name__ == '__main__':
    signal = HarmonicSerie(
        base_frequency=220.0,
        number_of_harmonics=30,
        harmonics_amplitude_function=lambda n: math.exp(-n / 2)
    )

    period = signal.period

    signal += WhiteNoise(amplitude=0.1)

    sample = signal.sample(
        t_min=0, t_max=3,
        frame_rate=44100
    )

    signal.plot(
        t_min=0, t_max=period, frame_rate=44100,
        xlabel="time (s)", ylabel="amplitude", title="", export_to="hs_plot.png"
    )

    sample.play(
        t_min=0.0, duration=3.0, frame_rate=44100,
        norm_to=0.1
    )
