from enum import StrEnum

class AudioProfile(StrEnum):
    """
    Codecs de audio de un archivo de audio.

    Attributes:
        AAC (str): Advanced Audio Coding, codec de audio con buena calidad a bajas tasas de bits.
        AAC_LOW (str): Variante de AAC con perfil de baja complejidad (LC-AAC).
        AAC_HE (str): High-Efficiency AAC, optimizado para bajas tasas de bits (HE-AAC v1).
        AC3 (str): Audio Coding 3, codec de audio Dolby Digital usado en DVD y cine.
        EAC3 (str): Enhanced AC-3, versión mejorada de Dolby Digital Plus.
        MP3 (str): MPEG-1 Audio Layer III, codec de audio muy popular y ampliamente usado.
        OPUS (str): Codec de audio versátil y libre de regalías, ideal para streaming.
        LIBOPUS (str): Implementación de referencia de Opus a través de la biblioteca libopus.
        VORBIS (str): Codec de audio libre, abierto y sin patentes, frecuente en Ogg containers.
        LIBVORBIS (str): Implementación de referencia de Vorbis a través de libvorbis.
        LIBFDK_AAC (str): Implementación del codec AAC usando la biblioteca FDK (alta calidad).
        FLAC (str): Free Lossless Audio Codec, codec sin pérdida de calidad.
        LIBFLAC (str): Implementación de referencia de FLAC a través de libflac.
    """
    AAC = "aac"
    AAC_LOW = "aac_low"
    AAC_HE = "aac_he"
    AC3 = "ac3"
    EAC3 = "eac3"
    MP3 = "mp3"
    OPUS = "opus"
    LIBOPUS = "libopus"
    VORBIS = "vorbis"
    LIBVORBIS = "libvorbis"
    LIBFDK_AAC = "libfaac"
    FLAC = "flac"
    LIBFLAC = "libflac"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value