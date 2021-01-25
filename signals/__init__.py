"""
    SoundSynthesis is a little package made to create sound signals from various type of signals
    Here is the different types of signal already implemented in the package :
    - GaussianNoise
    - WhiteNoise
    - Sine
    - HarmonicSerie
    - Envelop
"""

from .core import Signal, PeriodicSignal, SignalSum, SimpleSignal
from .GaussianNoise import GaussianNoise
from .WhiteNoise import WhiteNoise
from .Sine import Sine
from .HarmonicSerie import HarmonicSerie
from .Envelop import Envelop
from .AmplitudeModulation import AmplitudeModulation
