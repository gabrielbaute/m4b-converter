import uuid
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field, computed_field


class ConversionResult(BaseModel):
    """
    Contiene las métricas y resultados finales tras una conversión exitosa.

    Este modelo encapsula toda la información generada durante el proceso de conversión, incluyendo métricas de rendimiento, compresión y detalles del archivo resultante. Es utilizado para reportar resultados en la CLI y para seguimiento en procesos por lotes.

    Attributes:
        task_id (uuid.UUID): Identificador único de la tarea de conversión.
        output_path (Path): Ruta al archivo M4B generado.
        duration_seconds (float): Duración total del audio en segundos.
        size_original_bytes (int): Tamaño del archivo original en bytes.
        size_final_bytes (int): Tamaño del archivo convertido en bytes.
        bitrate_final (str): Bitrate final aplicado (ej: "64k", "128k").
        codec_final (str): Códec utilizado en el archivo final. Por defecto "aac" para M4B.
        timestamp_start (datetime): Momento de inicio de la conversión.
        timestamp_end (datetime): Momento de finalización de la conversión.

    Computed Properties:
        compression_ratio (float): Ratio de compresión calculado como 1 - (tamaño_final / tamaño_original). Indica el porcentaje de reducción (0.0 = sin compresión, 1.0 = compresión total).
        space_saved_mb (float): Espacio ahorrado en megabytes, calculado como la diferencia entre el tamaño original y el final.

    Example:
        >>> from datetime import datetime
        >>> import uuid
        >>> from pathlib import Path
        >>>
        >>> result = ConversionResult(
        ...     task_id=uuid.uuid4(),
        ...     output_path=Path("audiolibro.m4b"),
        ...     duration_seconds=3600.0,
        ...     size_original_bytes=50_000_000,  # ~47.7 MB
        ...     size_final_bytes=15_000_000,     # ~14.3 MB
        ...     bitrate_final="64k",
        ...     timestamp_start=datetime.now(),
        ...     timestamp_end=datetime.now()
        ... )
        >>>
        >>> print(f"Compresión: {result.compression_ratio*100:.1f}%")  # 70.0%
        >>> print(f"Espacio ahorrado: {result.space_saved_mb:.1f} MB")  # 33.4 MB

    Note:
        - `compression_ratio` y `space_saved_mb` son propiedades calculadas automáticamente y no requieren almacenamiento en la base de datos.
        - El ratio de compresión se redondea a 2 decimales para mayor claridad.
        - `codec_final` tiene "aac" como valor por defecto, que es el estándar para archivos M4B.
        - Si el tamaño original es 0, `compression_ratio` retorna 0.0 para evitar división por cero.
    """
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
        """
        Calcula el ratio de compresión (1 - final/original).

        Retorna:
            float: Ratio de compresión entre 0.0 y 1.0.
                - 0.0 = sin compresión (mismo tamaño)
                - 0.5 = 50% de reducción
                - 1.0 = compresión total (tamaño final 0)

        Note:
            Si el tamaño original es 0, retorna 0.0 para evitar división por cero.
        """
        if self.size_original_bytes == 0:
            return 0.0
        return round(1 - (self.size_final_bytes / self.size_original_bytes), 2)

    @computed_field
    @property
    def space_saved_mb(self) -> float:
        """
        Calcula el espacio ahorrado en Megabytes.

        Retorna:
            float: Espacio ahorrado en MB, redondeado a 2 decimales. Siempre será positivo o cero (no puede ser negativo).

        Note:
            Si el archivo final es más grande que el original (por ejemplo, al convertir a un bitrate más alto), este valor sería negativo. En el contexto de esta aplicación, siempre se espera que sea positivo debido a la compresión.
        """
        return round((self.size_original_bytes - self.size_final_bytes) / (1024 * 1024), 2)