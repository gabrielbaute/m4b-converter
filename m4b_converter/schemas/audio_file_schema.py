from typing import Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from m4b_converter.enums import Format, Bitrate
from m4b_converter.schemas.audio_metadata_schema import AudioMetadata


class AudioFileSchema(BaseModel):
    """
    Esquema Pydantic para la representación estructurada de un archivo de audio.

    Este modelo define la estructura de datos normalizada que utiliza la aplicación para trabajar con archivos de audio. Los datos provienen principalmente de ffprobe y son validados y transformados para garantizar su consistencia.

    El esquema incluye tanto propiedades técnicas del archivo (formato, codec, bitrate, etc.) como metadatos extraídos de las etiquetas del archivo.

    Attributes:
        path (Path): Ruta al archivo de audio en el sistema de archivos.
        size_bytes (int): Tamaño del archivo en bytes. Mapeado del campo 'size'.
        format_name (Format): Formato del contenedor del archivo (MP3, M4A, etc.).
        duration_seconds (float): Duración total del audio en segundos. Mapeado del campo 'duration'.
        codec (str): Códec de audio utilizado (ej: "mp3", "aac", "flac"). Mapeado del campo 'codec_name'.
        bitrate_kbps (int): Bitrate del audio en kilobits por segundo. Mapeado del campo 'bit_rate' y convertido de bps a kbps.
        sample_rate (int): Frecuencia de muestreo en Hz (ej: 44100, 48000).
        channels (int): Número de canales de audio (1=mono, 2=estéreo).
        metadata (AudioMetadata): Metadatos extraídos de las etiquetas del archivo (título, artista, álbum, etc.).

    Example:
        >>> from pathlib import Path
        >>> from m4b_converter.schemas import AudioFileSchema
        >>>
        >>> # Los datos normalmente vienen de ffprobe
        >>> data = {
        ...     "path": Path("audio.mp3"),
        ...     "size": 5242880,
        ...     "format_name": "mp3",
        ...     "duration": 180.5,
        ...     "codec_name": "mp3",
        ...     "bit_rate": "128000",
        ...     "sample_rate": 44100,
        ...     "channels": 2,
        ...     "metadata": {"title": "Mi Canción", "artist": "Artista"}
        ... }
        >>>
        >>> schema = AudioFileSchema(**data)
        >>> print(schema.bitrate_kbps)  # 128 (convertido desde 128000)
        >>> print(schema.duration_seconds)  # 180.5
        >>> print(schema.metadata.title)  # "Mi Canción"

    Note:
        - Los campos `size_bytes`, `duration_seconds`, `codec` y `bitrate_kbps` utilizan alias para mapear correctamente los nombres de campo de ffprobe.
        - El validador `parse_ffmpeg_format` maneja el caso especial donde ffprobe devuelve múltiples formatos separados por comas.
        - El validador `parse_bitrate` convierte el bitrate de bps (entero) a kbps.
    """

    path: Path
    size_bytes: int = Field(..., alias="size")
    format_name: Format
    duration_seconds: float = Field(..., alias="duration")
    codec: str = Field(..., alias="codec_name")
    bitrate_kbps: int = Field(..., alias="bit_rate")
    sample_rate: int
    channels: int
    metadata: AudioMetadata

    @field_validator("format_name", mode="before")
    @classmethod
    def parse_ffmpeg_format(cls, v: Any) -> str:
        """
        Valida y normaliza el nombre del formato del archivo.

        ffprobe puede devolver múltiples formatos separados por comas (ej: "mov,mp4,m4a,3gp,3g2,mj2"). Este validador selecciona el primer formato que coincida con los definidos en el enum Format.

        Args:
            v (Any): Valor del campo 'format_name' proveniente de ffprobe.

        Returns:
            str: Nombre del formato normalizado para el enum Format.

        Example:
            >>> AudioFileSchema.parse_ffmpeg_format("mov,mp4,m4a")
            'm4a'
            >>> AudioFileSchema.parse_ffmpeg_format("mp3")
            'mp3'
        """
        # ffprobe a veces devuelve "mov,mp4,m4a,3gp,3g2,mj2"
        if isinstance(v, str) and "," in v:
            parts = v.split(",")
            for p in parts:
                if p in [f.value for f in Format]:
                    return p
            return parts[0]
        return v

    @field_validator("bitrate_kbps", mode="before")
    @classmethod
    def parse_bitrate(cls, v: Any) -> int:
        """
        Convierte el bitrate de bits por segundo a kilobits por segundo.

        ffprobe devuelve el bitrate como un string en bps (ej: "128000"). Este validador convierte el valor a kbps dividiendo por 1000.

        Args:
            v (Any): Valor del campo 'bit_rate' proveniente de ffprobe.

        Returns:
            int: Bitrate en kilobits por segundo (kbps).

        Example:
            >>> AudioFileSchema.parse_bitrate("128000")
            128
            >>> AudioFileSchema.parse_bitrate("320000")
            320
            >>> AudioFileSchema.parse_bitrate(None)
            0
        """
        # El bitrate viene como string en el JSON de ffprobe ("320000")
        try:
            return int(v) // 1000
        except (ValueError, TypeError):
            return 0