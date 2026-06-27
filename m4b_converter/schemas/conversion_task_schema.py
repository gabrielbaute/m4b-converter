import uuid
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field


class ConversionTask(BaseModel):
    """
    Define la intención y parámetros de una conversión.

    Este modelo representa una tarea de conversión pendiente o en curso, capturando todos los parámetros necesarios para ejecutar la conversión. Se utiliza para el seguimiento y la trazabilidad de las operaciones.

    Attributes:
        id (uuid.UUID): Identificador único de la tarea. Se genera automáticamente con uuid.uuid4 si no se proporciona.
        input_path (Path): Ruta al archivo de audio de origen.
        timestamp_start (datetime): Momento en que se creó la tarea. Se establece automáticamente al momento de la instanciación.
        bitrate_target (str): Bitrate objetivo para la conversión (ej: "64k", "96k", "128k").
        channels_target (int): Número de canales de audio objetivo (1 = mono, 2 = estéreo).

    Example:
        >>> from pathlib import Path
        >>> from m4b_converter.schemas import ConversionTask
        >>>
        >>> # Crear tarea con parámetros manuales
        >>> task = ConversionTask(
        ...     input_path=Path("audiolibro.mp3"),
        ...     bitrate_target="64k",
        ...     channels_target=1
        ... )
        >>>
        >>> print(f"Tarea: {task.id}")
        >>> print(f"Origen: {task.input_path}")
        >>> print(f"Bitrate: {task.bitrate_target}")
        >>> print(f"Canales: {task.channels_target}")

    Note:
        - `id` y `timestamp_start` se generan automáticamente usando default_factory para simplificar la creación de tareas.
        - Esta tarea se pasa a `M4bConverterService.convert()` para ejecutar la conversión real.
        - El resultado de la conversión se devuelve como `ConversionResult`.

    See Also:
        - `ConversionResult`: Modelo que contiene los resultados de la tarea.
        - `M4bConverterService`: Servicio que ejecuta las tareas.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    input_path: Path
    timestamp_start: datetime = Field(default_factory=datetime.now)
    bitrate_target: str
    channels_target: int