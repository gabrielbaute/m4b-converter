from typing import Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from m4b_converter.enums import Format, Bitrate
from m4b_converter.schemas.audio_metadata_schema import AudioMetadata


class AudioFileSchema(BaseModel):
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
        # El bitrate viene como string en el JSON de ffprobe ("320000")
        try:
            return int(v) // 1000
        except (ValueError, TypeError):
            return 0