#!/usr/bin/env python
"""
SoundSynthesis is a little package made to create sound signals from various type of signals

Here is the different types of signal already implemented in the package :
    - GaussianNoise
    - WhiteNoise
    - Sine
    - Cosine
    - HarmonicSerie
    - Envelop
    - AmplitudeModulation
"""
from .core import Signal, PeriodicSignal, SignalSum, SimpleSignal
from .GaussianNoise import GaussianNoise
from .WhiteNoise import WhiteNoise
from .Sine import Sine
from .Cosine import Cosine
from .HarmonicSerie import HarmonicSerie
from .Envelop import Envelop
from .AmplitudeModulation import AmplitudeModulation
from .Click import Click
from .FunctionSignal import FunctionSignal

# metadata
__author__ = "Gabriel Amare"
__author_email__ = "gabriel.amare.31@gmail.com"
__version__ = "1.0"
__url__ = "https://github.com/GabrielAmare/SoundSynthesis"
__longdescr__ = """
SoundSynthesis is a little package made to create sound signals from various type of signals

Here is the different types of signal already implemented in the package :
    - GaussianNoise
    - WhiteNoise
    - Sine
    - Cosine
    - HarmonicSerie
    - Envelop
    - AmplitudeModulation
    - Click
    - FunctionSignal
"""
__classifiers__ = [
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis"
]
