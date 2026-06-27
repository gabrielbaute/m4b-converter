import json
import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any

from m4b_converter.schemas import AudioFileSchema

class AudioAnalyzerService:
    """
    Servicio para analizar archivos de audio utilizando ffprobe.

    Esta clase proporciona funcionalidades para extraer información detallada de archivos de audio mediante el uso de ffprobe, incluyendo metadatos, formato, codecs, duración y características técnicas del audio.

    El servicio es utilizado como paso inicial en el flujo de conversión para obtener los datos necesarios para la transformación a M4B.

    Attributes:
        file_path (Path): Ruta al archivo de audio a analizar.
        logger (logging.Logger): Logger para registrar eventos y errores.
        _raw_data (Dict[str, Any]): Datos crudos obtenidos de ffprobe en formato JSON.

    Example:
        >>> from pathlib import Path
        >>> analyzer = AudioAnalyzerService(Path("audio.mp3"))
        >>> info = analyzer.analyze()
        >>> print(info.format_name)
        'mp3'
    """
    def __init__(self, file_path: Path):
        """
        Inicializa el servicio de análisis de audio.

        Args:
            file_path (Path): Ruta al archivo de audio que se desea analizar. El archivo debe existir y ser accesible.

        Raises:
            FileNotFoundError: Si el archivo no existe en la ruta especificada.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file_path = file_path
        self._raw_data = self.get_raw_info()

    def get_raw_info(self) -> Dict[str, any]:
        """
        Ejecuta ffprobe y retorna los datos crudos en formato diccionario.

        Este método utiliza ffprobe para extraer toda la información disponible del archivo de audio, incluyendo formato, streams y metadatos.

        Returns:
            Dict[str, Any]: Diccionario con la información completa extraída por ffprobe. Contiene las secciones 'format' y 'streams' con todos los detalles técnicos del archivo. Retorna un diccionario vacío si ocurre un error.

        Raises:
            subprocess.CalledProcessError: Si ffprobe no se ejecuta correctamente (el error es capturado y se retorna un diccionario vacío).
            json.JSONDecodeError: Si la salida de ffprobe no es JSON válido (el error es capturado y se retorna un diccionario vacío).

        Note:
            Este método asume que ffprobe está instalado en el sistema y accesible desde la línea de comandos.
        """
        cmd = [
            "ffprobe", "-v", "error", 
            "-show_format", "-show_streams", "-print_format", "json", 
            str(self.file_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.logger.error(f"Error analizando archivo: {e}")
            return {}

    def _get_raw_format_info(self) -> Dict:
        """
        Obtiene la información de formato del archivo desde los datos crudos.

        Returns:
            Dict[str, Any]: Diccionario con la información de formato del archivo. Incluye datos como duración, tamaño, bitrate general y nombre del formato. Retorna un diccionario vacío si no hay datos disponibles.
        """
        return self._raw_data.get("format", {})
    
    def _get_raw_streams_info(self) -> List[Dict]:
        """
        Obtiene la información de los streams del archivo desde los datos crudos.

        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con la información de cada stream. Generalmente incluye streams de audio, y opcionalmente de video (portadas). Retorna una lista vacía si no hay streams disponibles.
        """
        return self._raw_data.get("streams", [])
        
    def analyze(self) -> Optional[AudioFileSchema]:
        """
        Analiza el archivo de audio y mapea la información al esquema Pydantic.

        Este método procesa los datos crudos obtenidos de ffprobe y los estructura en un objeto AudioFileSchema validado, que contiene toda la información relevante para el proceso de conversión.

        Returns:
            Optional[AudioFileSchema]: Objeto AudioFileSchema con la información estructurada del archivo de audio. Retorna None si:
                - No se pudieron obtener datos crudos del archivo.
                - Ocurre un error durante la validación de los datos.

        Raises:
            ValidationError: Si los datos extraídos no cumplen con el esquema definido (el error es capturado y se retorna None).

        Note:
            Los metadatos del archivo se extraen de las etiquetas (tags) y se filtran automáticamente por el esquema AudioMetadata.

        Example:
            >>> analyzer = AudioAnalyzerService(Path("mi_audiolibro.mp3"))
            >>> info = analyzer.analyze()
            >>> if info:
            ...     print(f"Duración: {info.duration_seconds}s")
            ...     print(f"Bitrate: {info.bitrate_kbps} kbps")
        """
        if not self._raw_data:
            return None

        format_info = self._get_raw_format_info()
        streams = self._get_raw_streams_info()
        
        # Buscamos el primer stream de audio
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
        
        # Combinamos datos para el Schema
        data_for_schema = {
            "path": self.file_path,
            "size": format_info.get("size"),
            "format_name": format_info.get("format_name"),
            "duration": format_info.get("duration"),
            "codec_name": audio_stream.get("codec_name"),
            "bit_rate": audio_stream.get("bit_rate") or format_info.get("bit_rate"),
            "sample_rate": audio_stream.get("sample_rate"),
            "channels": audio_stream.get("channels"),
            "metadata": format_info.get("tags", {}) # Filtramos los tags con Pydantic
        }

        try:
            return AudioFileSchema(**data_for_schema)
        except Exception as e:
            self.logger.error(f"Error validando datos con Pydantic: {e}")
            return None

    @property
    def raw_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos crudos del archivo de audio analizado.

        Esta propiedad permite acceder a los datos JSON completos obtenidos de ffprobe sin procesar, útil para inspección o depuración avanzada.

        Returns:
            Dict[str, Any]: Diccionario completo con los datos crudos del archivo. Contiene las secciones 'format' y 'streams' sin modificar.

        Example:
            >>> analyzer = AudioAnalyzerService(Path("audio.mp3"))
            >>> raw = analyzer.raw_data
            >>> streams = raw.get("streams", [])
            >>> # Inspeccionar streams directamente
        """
        return self._raw_data