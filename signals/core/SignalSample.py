import os
import sys
import struct
import wave
import random
import numpy as np
from .playsound import playsound

try:
    import matplotlib.pyplot as plt
except:
    plt = None

from .utils import grouper

from .TimeSample import TimeSample


class SignalSample:
    temp_wave_filepath = "temp.wav"

    @classmethod
    def from_signal(cls, time_sample, signal):
        return cls(time_sample=time_sample, Y=signal.sample_data(time_sample))

    def __init__(self, time_sample: TimeSample, Y):
        assert len(time_sample) == len(Y)
        self.time_sample = time_sample
        self.Y = Y

    def plot(self, title: str = "", xlabel: str = "", ylabel: str = "", export_to: str = None):
        """
            :param title: the plot title
            :param xlabel: the label for the x axis (time axis)
            :param ylabel: the label for the y axis (amplitude axis)

            :param export_to: if you want to export the plot as an image, give it the desired filepath for the image
        """
        if not plt:
            raise Exception(f"To use the .plot method you must install `matplotlib` using the command : "
                            f"pip install matplotlib")

        fig, ax = plt.subplots()
        ax.plot(list(self.time_sample), self.Y)

        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        ax.grid()
        if export_to:
            fig.savefig(export_to)
        plt.show()

    def to_wave(self, filepath, norm_to=None, sampwidth=2, bufsize=2048):
        nchannels = 2

        data = self.Y

        if norm_to is not None:
            data = list(data)
            amplitude_max = max(map(abs, data))
            data = ((norm_to * amplitude) / amplitude_max for amplitude in data)

        samples = [data]

        with wave.open(filepath, 'w') as file:
            file.setparams((nchannels, sampwidth, self.time_sample.frame_rate, self.time_sample.n_frames, 'NONE',
                            'not compressed'))

            bin_size = 2 ** (sampwidth * 8)

            max_amplitude = float(int(bin_size / 2) - 1)

            def bounds(value):
                if value < -bin_size // 2:
                    return -bin_size // 2
                elif value >= bin_size // 2:
                    return bin_size // 2 - 1
                else:
                    return value

            for chunk in grouper(bufsize, samples):
                frames = b''.join(
                    b''.join(
                        struct.pack('h', int(bounds(max_amplitude * sample))) for sample in channels
                    ) for channels in chunk if channels is not None
                )
                file.writeframesraw(frames)

    def play(self, block=True, **config):
        fp = ""
        while not fp or os.path.exists(fp):
            fp = f"temp_{random.random()}.wav"

        try:
            self.to_wave(fp, **config)
        except Exception as e:
            if os.path.exists(fp):
                os.remove(fp)
            raise e

        playsound(fp, block=block)

        try:
            os.remove(fp)
        except:
            print("The temp file haven't been deleted properly !", file=sys.stderr)
