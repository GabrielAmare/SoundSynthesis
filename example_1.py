from signals import *
import math
"""
    Harmonic serie with noise, sampled, saved and played
"""

if __name__ == '__main__':
    # we create the harmonic serie
    harmonic_serie = HarmonicSerie(
        base_frequency=220.0,
        number_of_harmonics=30,
        harmonics_amplitude_function=lambda n: math.exp(-n / 2)
    )

    # and we add some noise to it (stored in a different variable `harmonic_serie_with_noise` )
    harmonic_serie_with_noise = harmonic_serie + WhiteNoise(amplitude=0.075)

    # we plot the `harmonic_serie` for one period
    harmonic_serie.plot(
        duration=harmonic_serie.period,
        frame_rate=44100,
        xlabel="time (s)",
        ylabel="amplitude",
        title="One period of the harmonic serie with white noise"
    )

    # we sample the `harmonic_serie_with_noise` for 3 seconds
    sample = harmonic_serie_with_noise.sample(
        duration=3,
        frame_rate=44100
    )

    # then we play the sample (normalized to 0.1)
    sample.play(norm_to=0.1)

    # and we store it as a wav file
    sample.to_wave(filepath="harmonic serie with noise.wav", norm_to=0.1)
