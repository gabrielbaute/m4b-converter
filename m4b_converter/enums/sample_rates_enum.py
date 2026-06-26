from enum import IntEnum

class SampleRate(IntEnum):
    """
    Tasa de sampleo de un archivo de audio.

    Attributes:
        SR_22050 (int): 22 KHz
        SR_44100 (int): 44 KHz
        SR_48000 (int): 48 KHz
    """
    SR_22050 = 22050
    SR_44100 = 44100
    SR_48000 = 48000

    def __str__(self):
        return self.value