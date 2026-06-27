"""
Esquemas Pydantic para la validación y estructuración de datos.

Este paquete contiene los modelos de datos utilizados en toda la aplicación para garantizar la consistencia y validación de la información en cada etapa del proceso de conversión.
"""
from m4b_converter.schemas.audio_file_schema import AudioFileSchema
from m4b_converter.schemas.audio_metadata_schema import AudioMetadata
from m4b_converter.schemas.conversion_task_schema import ConversionTask
from m4b_converter.schemas.conversion_result_schema import ConversionResult

__all__ = [
    "AudioFileSchema",
    "AudioMetadata", 
    "ConversionTask",
    "ConversionResult"
]