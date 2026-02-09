from enum import IntEnum

class SampleRate(IntEnum):
    SR_22050 = 22050
    SR_44100 = 44100
    SR_48000 = 48000

    def __str__(self):
        return self.value