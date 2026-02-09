from typing import Optional
from pydantic import BaseModel, Field, AliasChoices

class AudioMetadata(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    track: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    comment: Optional[str] = None
    # Usamos AliasChoices por si el tag viene como 'lyrics-eng' o 'description'
    description: Optional[str] = Field(None, validation_alias=AliasChoices('lyrics-eng', 'description'))
