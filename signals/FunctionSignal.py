from .core import Signal


class FunctionSignal(Signal):
    def __init__(self, function):
        self.function = function

    def __call__(self, t):
        return self.function(t)
