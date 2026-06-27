from typing import Optional
from pydantic import BaseModel, Field, AliasChoices


class AudioMetadata(BaseModel):
    """
    Esquema Pydantic para los metadatos de un archivo de audio.

    Este modelo define la estructura de metadatos que puede contener un archivo de audio, extrayendo información de las etiquetas (tags) comunes como ID3 en MP3 o Vorbis comments en FLAC/OGG.

    Todos los campos son opcionales ya que los archivos de audio pueden no contener todos los metadatos. El modelo está diseñado para ser flexible y manejar diferentes estándares de etiquetado.

    Attributes:
        title (Optional[str]): Título de la pista o audiolibro.
        artist (Optional[str]): Nombre del artista, narrador o autor.
        album (Optional[str]): Álbum o nombre de la colección.
        track (Optional[str]): Número de pista o posición en el álbum.
        genre (Optional[str]): Género musical o categoría del contenido.
        date (Optional[str]): Fecha de publicación o año.
        comment (Optional[str]): Comentarios o notas adicionales.
        description (Optional[str]): Descripción del contenido. Se mapea desde diferentes campos de origen como 'lyrics-eng' (común en audiolibros para descripción) o 'description'.

    Example:
        >>> from m4b_converter.schemas import AudioMetadata
        >>>
        >>> # Crear metadatos manualmente
        >>> meta = AudioMetadata(
        ...     title="El Principito",
        ...     artist="Antoine de Saint-Exupéry",
        ...     album="Audiolibros Clásicos",
        ...     genre="Ficción",
        ...     date="1943",
        ...     description="Un clásico de la literatura infantil"
        ... )
        >>>
        >>> # Acceder a los campos
        >>> print(meta.title)  # "El Principito"
        >>> print(meta.description)  # "Un clásico de la literatura infantil"

    Note:
        - El campo `description` utiliza `AliasChoices` para poder mapearse desde diferentes nombres de campo que ffprobe puede devolver.
        - 'lyrics-eng' es común en archivos M4A/M4B para almacenar la descripción del audiolibro.
        - Todos los campos son opcionales para manejar archivos sin etiquetas.
        - Los nombres de los campos coinciden con los metadatos estándar de ffprobe para facilitar el mapeo directo.

    See Also:
        - `AudioFileSchema`: Esquema principal que contiene este modelo.
    """

    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    track: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    comment: Optional[str] = None
    # Usamos AliasChoices por si el tag viene como 'lyrics-eng' o 'description'
    description: Optional[str] = Field(
        None,
        validation_alias=AliasChoices('lyrics-eng', 'description'),
        description="Descripción del audiolibro. Se mapea desde 'lyrics-eng' (común en M4B) o 'description' (estándar en otros formatos)."
    )