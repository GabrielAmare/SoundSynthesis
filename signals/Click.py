from .core import Signal


class Click(Signal):
    def __init__(self, t_min: float, t_max: float, amplitude: float = 1.0):
        """
            Create white noise for a random uniform distribution law between [-amplitude, +amplitude]
        :param amplitude: The maximum amplitude of the signal
        """
        self.t_min, self.t_max = min(t_min, t_max), max(t_min, t_max)
        self.amplitude = abs(amplitude)

    def __call__(self, t):
        if self.t_min <= t <= self.t_max:
            return self.amplitude
        else:
            return 0

    def __repr__(self):
        return f"{self.amplitude} * ({self.t_min} <= t <= {self.t_max})"
