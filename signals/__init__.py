"""
    SoundSynthesis is a little package made to create sound signals from various type of signals
    Here is the different types of signal already implemented in the package :
    - GaussianNoise
    - WhiteNoise
    - Sine
    - HarmonicSerie
    - Envelop
"""

from .Signal import Signal
from .GaussianNoise import GaussianNoise
from .WhiteNoise import WhiteNoise
from .Sine import Sine
from .HarmonicSerie import HarmonicSerie
from .Envelop import Envelop
