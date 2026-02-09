import uuid
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field, computed_field

class ConversionResult(BaseModel):
    """Contiene las métricas finales tras la conversión."""
    task_id: uuid.UUID
    output_path: Path
    duration_seconds: float
    size_original_bytes: int
    size_final_bytes: int
    bitrate_final: str
    codec_final: str = "aac"
    timestamp_start: datetime = Field(default_factory=datetime.now)
    timestamp_end: datetime

    @computed_field
    @property
    def compression_ratio(self) -> float:
        """Calcula el ratio de compresión (1 - final/original)."""
        if self.size_original_bytes == 0:
            return 0.0
        return round(1 - (self.size_final_bytes / self.size_original_bytes), 2)

    @computed_field
    @property
    def space_saved_mb(self) -> float:
        """Espacio ahorrado en Megabytes."""
        return round((self.size_original_bytes - self.size_final_bytes) / (1024 * 1024), 2)