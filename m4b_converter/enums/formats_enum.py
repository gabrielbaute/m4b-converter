from enum import StrEnum

class Format(StrEnum):
    """
    Enum para los formatos de audio compatibles con audiolibros.

    Attributes:
        MP3 (str): MP3 - Formato universal y ampliamente compatible, buena relación calidad/tamaño para audiolibros.
        M4B (str): M4B - Formato específico para audiolibros basado en MP4, soporta marcadores, capítulos y persistencia de posición.
        M4A (str): M4A - Formato de audio MP4 sin DRM, ideal para audiolibros con codificación AAC, similar a M4B pero sin características de libro.
        WAV (str): WAV - Formato de audio sin comprimir, calidad lossless pero archivos grandes, usado para masterización y edición.
        OPUS (str): OPUS - Codec moderno y eficiente, excelente para streaming y buena calidad en bajos bitrates.
        OGG (str): OGG - Contenedor abierto que usa codec Vorbis, buena alternativa libre para audiolibros.
        FLAC (str): FLAC - Formato sin pérdida de calidad, ideal para archivar y preservar la calidad original de grabaciones.
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