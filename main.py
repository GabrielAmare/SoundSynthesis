"""
    SoundSynthesis is a little module made to create sounds from sines
"""
import math
import random
import wave
import struct
import itertools
import playsound  # to install


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


class Signal:
    temp_wave_filepath = "temp.wav"

    def __call__(self, t):
        """
            For a given time (in seconds) return the corresponding height of the signal
        :param t: The time (in seconds)
        :return: The intensity of the signal at that time
        """
        raise NotImplementedError

    def sample(self, frame_rate: float, n_frames: int, offset: float = 0.0):
        """
        Return a sample of the signal
        :param frame_rate: the rate of frames per second
        :param n_frames: the number of frames wanted for the sample
        :param offset: the offset (between 0 and 1) (if you don't know, don't touch, even if it shoudn't change anything in practice)
        :return: the desired sample of the signal, in the form of a list of floats
        """
        assert 0 <= offset <= 1

        for i_frame in range(n_frames):
            yield self((i_frame + offset) / frame_rate)

    def sample_enum(self, frame_rate, n_frames, offset=0):
        """
        Return a sample of the coordinates (t, signal(t))
        -> see the Signal.sample method for details on the params
        :return: the desired coordinates sample
        """
        assert 0 <= offset <= 1
        for i_frame, y in enumerate(self.sample(frame_rate, n_frames)):
            yield i_frame / frame_rate, y

    def add_whitenoise(self, amplitude):
        """
            Return the current signal where some whitenoise has been added
        :param amplitude: See WhiteNoise.__init__ docstring
        :return: self + whitenoise
        """
        whitenoise = WhiteNoise(amplitude=amplitude)
        return SignalSum(self, whitenoise)

    def add_sine(self, frequency, amplitude=1.0, phase=0.0):
        """
            Return the current signal where some sine has been added
        :param frequency: See Sine.__init__ docstring
        :param amplitude: See Sine.__init__ docstring
        :param phase: See Sine.__init__ docstring
        :return: self + sine
        """
        sine = Sine(amplitude=amplitude, frequency=frequency, phase=phase)
        return SignalSum(self, sine)

    def to_wave(self, filename, n_frames=None, duration=None, frame_rate=44100, sampwidth=2, bufsize=2048):
        """
            Allow to create a wave file from the signal (given the sample params and the wave params)
        :param filename: The name of the file to save
        :param n_frames: see Signal.sample method docstring
        :param frame_rate: see Signal.sample method docstring
        :param duration: you can provide duration instead of n_frames OR frame_rate (the calculation for the missing param will be done automatically)
        :param sampwidth: The sample width (number of bytes for the amplitude)
        :param bufsize: The size of the buffer used to write the wave file (used to reduce memory consumption and improve performances)
        :return: None (to access the file use it's filename
        """
        if n_frames is None and duration is not None and frame_rate is not None:
            n_frames = int(duration * frame_rate)
        elif n_frames is not None and duration is None and frame_rate is not None:
            duration = n_frames * frame_rate
        elif n_frames is not None and duration is not None and frame_rate is None:
            frame_rate = duration / n_frames
        else:
            raise Exception(
                f"{self.__class__.__name__}.to_wave(...) : You have to specify two parameters of ('n_frames', 'duration', 'frame_rate')")

        assert n_frames % 1 == 0

        n_frames = int(n_frames)
        frame_rate = float(frame_rate)

        nchannels = 2

        sample = self.sample(frame_rate=frame_rate, n_frames=n_frames, offset=0)

        samples = [sample]

        with wave.open(filename, 'w') as file:
            file.setparams((nchannels, sampwidth, frame_rate, n_frames, 'NONE', 'not compressed'))

            bin_size = 2 ** (sampwidth * 8)

            max_amplitude = float(int(bin_size / 2) - 1)

            for chunk in grouper(bufsize, samples):
                frames = b''.join(
                    b''.join(
                        struct.pack('h', int(max_amplitude * sample)) for sample in channels
                    ) for channels in chunk if channels is not None
                )
                file.writeframesraw(frames)

    def play(self, duration, **config):
        """
            Play the sound for a given duration (save a temporary file, play it)
        :param duration: Duration in seconds
        :return: None
        """
        filepath = self.__class__.temp_wave_filepath

        self.to_wave(filepath, duration=duration, **config)

        playsound.playsound(filepath)

        # TODO : os.remove(filepath) doesn't work properly here.
        #  I guess it's because playsound doesn't close the filestream of something like that.
        #  The temp.wav file shouldn't remain after the program lifetime.


class WhiteNoise(Signal):
    def __init__(self, amplitude: float):
        """
            Create white noise for a random uniform distribution law between [-amplitude, +amplitude]
        :param amplitude: The maximum amplitude of the signal
        """
        self.amplitude = math.fabs(amplitude)

    def __repr__(self):
        """Displays the white noise equation (where U is used as an abbreviation for random uniform distribution)"""
        return f"U(-{self.amplitude}, {self.amplitude})"

    def __call__(self, t):
        """
            See Signal.__call__ docstring
            >>> help(Signal.__init__)
        """
        return self.amplitude * random.uniform(-1, 1)


class Sine(Signal):
    def __init__(self, frequency, amplitude=1.0, phase=0.0):
        """
            Create a sine wave of the form :   S(t) = A * sin(2 pi f t + p)   [where A = amplitude, f = frequency, p = phase, t = time]
        :param frequency: The frequency of the sine
        :param amplitude: The amplitude of the sine
        :param phase: The phase of the sine
        """
        assert frequency != 0, "Sine.__init__, frequency shall not be 0"
        self.amplitude = amplitude  # m
        self.frequency = frequency  # 1/s
        self.phase = phase  # m (if the phase is a function, it will be called on t when self is called)

    def __repr__(self):
        """Displays the sine equation"""
        result = ""

        amplitude = round(self.amplitude, 3)
        frequency = round(self.frequency, 3)
        phase = round(self.phase, 3)

        if amplitude != 1:
            result += f"{amplitude}*"

        if frequency != 1:
            result += f"sin(2*π*{frequency}*t"
        else:
            result += f"sin(2*π*t"

        if isinstance(phase, (int, float)):
            if phase > 0:
                result += f" + {phase})"
            elif phase < 0:
                result += f" - {phase})"
        else:
            result += f" + {phase}"

        result += ")"

        return result

    def __call__(self, t):
        """
            See Signal.__call__ docstring
            >>> help(Signal.__init__)
        """
        return self.amplitude * math.sin(2 * math.pi * self.frequency * t + self.phase)


class SignalSum(Signal):
    def __init__(self, *sines):
        assert all(isinstance(sine, Signal) for sine in sines)
        self.sines = list(sines)

    def __repr__(self):
        return " + ".join(map(repr, self.sines))

    def __call__(self, t):
        if self.sines:
            return sum(sine(t) for sine in self.sines)
        else:
            return 0


def harmonic_serie(base_frequency, base_amplitude, factors):
    """
        Return a sum of the desired harmonics for a base_frequence at a base_amplitude
    :param frequency: The base frequency
    :param amplitude: The base amplitude
    :param factors: Some mapping {base_frequency_multiplier: base_amplitude_multiplier}
    :return: A sum of all the harmonics described
    """

    harmonics = []
    for base_frequency_multiplier, base_amplitude_multiplier in factors.items():
        sine = Sine(
            frequency=base_frequency * base_frequency_multiplier,
            amplitude=base_amplitude * base_amplitude_multiplier,
            phase=0
        )
        harmonics.append(sine)

    return SignalSum(*harmonics)


def harmonic_serie_func(base_frequency, base_amplitude, number_of_harmonics, function):
    """
        Return a sum of the desired harmonics for a base_frequence at a base_amplitude
    :param base_frequency: See the harmonic_serie docstring
    :param base_amplitude: See the harmonic_serie docstring
    :param number_of_harmonics: The number of harmonics to generate
    :param function: The function to generate the base_amplitude_multiplier from the base_frequency_multiplier
    :return:
    """
    factors = {}
    for base_frequency_multiplier in range(1, number_of_harmonics + 1):
        base_amplitude_multiplier = function(base_frequency_multiplier)
        factors[base_frequency_multiplier] = base_amplitude_multiplier

    return harmonic_serie(base_frequency, base_amplitude, factors)


if __name__ == '__main__':
    signal = WhiteNoise(amplitude=0.05).add_sine(440.0, amplitude=0.1)
    print(signal)
    signal.play(duration=2.0)
