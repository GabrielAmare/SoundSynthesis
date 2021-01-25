def are_defined(*values):
    """Used to know if params are defined in the signature"""
    return None not in values


class TimeSample:
    """Represent the discrete time sample based on params"""

    def __init__(self, t_min=None, t_max=None, duration=None, n_frames=None, frame_rate=None):
        """
            You can :
                - define at least 2 params of [`t_min`, `t_max`, `duration`] and either `n_frames` or `frame_rate`
                OR
                - define `n_frames` and `frame_rate` and one of `t_min` or `t_max`

            Here is a list of the accepted signatures :
                (t_min, t_max, n_frames)
                (t_min, t_max, frame_rate)
                (t_min, duration, n_frames)
                (t_min, duration, frame_rate)
                (t_max, duration, n_frames)
                (t_max, duration, frame_rate)
                (t_min, n_frames, frame_rate)
                (t_max, n_frames, frame_rate)
                (duration, n_frames, frame_rate)

            Each one of them can be used to define properly a TimeSample instance
        """
        self.t_min = t_min
        self.t_max = t_max
        self.duration = duration
        self.n_frames = n_frames
        self.frame_rate = frame_rate

        if are_defined(t_min, t_max):
            self.duration = t_max - t_min
            if are_defined(n_frames):
                self.frame_rate = self.duration / n_frames
            elif are_defined(frame_rate):
                self.n_frames = int(self.duration * frame_rate)
            else:
                raise Exception(f"Uncomplete definition ! {dict(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)}")
        elif are_defined(t_min, duration):
            self.t_max = t_min + duration
            if are_defined(n_frames):
                self.frame_rate = self.duration / n_frames
            elif are_defined(frame_rate):
                self.n_frames = int(self.duration * frame_rate)
            else:
                raise Exception(f"Uncomplete definition ! {dict(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)}")
        elif are_defined(t_max, duration):
            self.t_min = t_max - duration
            if are_defined(n_frames):
                self.frame_rate = self.duration / n_frames
            elif are_defined(frame_rate):
                self.n_frames = int(self.duration * frame_rate)
            else:
                raise Exception(f"Uncomplete definition ! {dict(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)}")
        elif are_defined(n_frames, frame_rate):
            self.duration = n_frames * frame_rate
            if are_defined(t_min):
                self.t_max = t_min + self.duration
            elif are_defined(t_max):
                self.t_min = t_max - self.duration
            else:
                raise Exception(f"Uncomplete definition ! {dict(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)}")
        else:
            raise Exception(f"Uncomplete definition ! {dict(t_min=t_min, t_max=t_max, duration=duration, n_frames=n_frames, frame_rate=frame_rate)}")

        self.frame_width = 1 / self.frame_rate

    def __iter__(self):
        for i_frame in range(self.n_frames):
            yield self.t_min + i_frame * self.frame_width

    def __len__(self):
        return self.n_frames
