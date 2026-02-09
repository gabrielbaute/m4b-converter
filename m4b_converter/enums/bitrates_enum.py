from enum import StrEnum

class Bitrate(StrEnum):
    """
    Enum para los bitrates
    """
    B_64K = "64k"
    B_96K = "96k"
    B_128K = "128k"
    B_192K = "192k"
    B_256K = "256k"
    B_320K = "320k"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value