from enum import StrEnum

class Format(StrEnum):
    """
    Enum para los formatos de audio.
    """
    MP3 = "mp3"
    M4B = "m4b"
    M4A = "m4a"
    WAV = "wav"
    OPUS = "opus"
    OGG = "ogg"
    FLAC = "flac"
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value