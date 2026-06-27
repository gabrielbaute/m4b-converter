"""
Enumeraciones para tipos de datos comunes en la conversión de audio.

Este paquete contiene todas las enumeraciones utilizadas en la aplicación para garantizar valores consistentes y tipados en formatos, bitrates, perfiles de audio, canales y frecuencias de muestreo.
"""
from m4b_converter.enums.formats_enum import Format
from m4b_converter.enums.bitrates_enum import Bitrate
from m4b_converter.enums.sample_rates_enum import SampleRate
from m4b_converter.enums.audio_profiles_enum import AudioProfile
from m4b_converter.enums.audio_channels_enum import AudioChannels

__all__ = [
    "Format",
    "Bitrate", 
    "SampleRate",
    "AudioProfile",
    "AudioChannels"
]