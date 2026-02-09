from enum import IntEnum

class AudioChannels(IntEnum):
    MONO = 1
    STEREO = 2
    
    def __str__(self):
        return self.value