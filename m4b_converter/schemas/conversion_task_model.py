import uuid
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field

class ConversionTask(BaseModel):
    """Define la intención de una conversión."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    input_path: Path
    timestamp_start: datetime = Field(default_factory=datetime.now)
    bitrate_target: str
    channels_target: int