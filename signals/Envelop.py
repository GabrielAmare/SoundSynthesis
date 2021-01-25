from .core import Signal


class Envelop(Signal):
    """
        Allow to envelop a signal and change it's amplitude depending on time
    """

    def __init__(self, original_signal, amplitude_function):
        self.original_signal = original_signal
        self.amplitude_function = amplitude_function

    @property
    def period(self):
        return 0

    def __call__(self, t):
        return self.amplitude_function(t) * self.original_signal(t)
