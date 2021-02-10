from .Signal import Signal, PeriodicSignal, SimpleSignal
from .SignalSum import SignalSum
from .SignalProd import SignalProd
from .utils import *

Signal.__add__ = Signal.__iadd__ = lambda self, other: SignalSum(self, other)
Signal.__mul__ = Signal.__imul__ = lambda self, other: SignalProd(self, other)

