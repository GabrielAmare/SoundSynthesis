from .Signal import Signal


class AmplitudeModulation(Signal):
    def __init__(self, carrier: Signal, carried: Signal, factor: float = 1):
        """
            Create an amplitude modulation
            :param carrier: carrier wave
            :param carried: carried wave
            :param factor: modulation factor
        """
        self.carrier = carrier  # xp = Ap sin(wp * t)
        self.carried = carried  # xm = Am sin(wm * t)
        self.factor = factor
        # TODO : find a way to rewrite factor as modulation_depth (which is include in [0, 1])
        #  to do so, we need to have the max_amplitude for any signal which can be `carrier` or `carried`

    def __call__(self, t):
        # xp + k * xp * xm = xp * (1 + k * xm)
        return self.carrier(t) * (1 + self.factor * self.carried(t))
