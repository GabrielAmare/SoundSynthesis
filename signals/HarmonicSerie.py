from .core import PeriodicSignal, SignalSum
from .Sine import Sine


class HarmonicSerie(PeriodicSignal):
    def __init__(self, base_frequency, number_of_harmonics,
                 harmonics_amplitude_function=None,
                 harmonics_phase_function=None):
        self.base_frequency = base_frequency
        self.number_of_harmonics = number_of_harmonics
        self.harmonics_amplitude_function = harmonics_amplitude_function
        self.harmonics_phase_function = harmonics_phase_function

        self.fundamental, *self.harmonics = (
            Sine(
                frequency=self.frequency_for(harmonic_number),
                amplitude=self.amplitude_for(harmonic_number),
                phase=self.phase_for(harmonic_number)
            )
            for harmonic_number in range(1, self.number_of_harmonics + 1)
        )

        self.signal = SignalSum(self.fundamental, *self.harmonics)

    @property
    def period(self):
        """The period of an harmonic serie is the period of the fundamental sine"""
        return self.fundamental.period

    def __call__(self, t):
        return self.signal(t)

    def __repr__(self):
        return f"HS({self.base_frequency}, {self.number_of_harmonics}, {self.harmonics_amplitude_function})"

    def frequency_for(self, harmonic_number):
        return self.base_frequency * harmonic_number

    def amplitude_for(self, harmonic_number):
        if self.harmonics_amplitude_function:
            return self.harmonics_amplitude_function(harmonic_number)
        else:
            return 1

    def phase_for(self, harmonic_number):
        if self.harmonics_phase_function:
            return self.harmonics_phase_function(harmonic_number)
        else:
            return 0
