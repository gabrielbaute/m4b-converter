import json
import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from m4b_converter.schemas import AudioFileSchema, AudioMetadata

class AudioAnalyzerService:
    def __init__(self, file_path: Path):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file_path = file_path
        self._raw_data = self.get_raw_info()

    def get_raw_info(self) -> Dict[str, any]:
        """
        Ejecuta ffprobe y retorna el dict crudo.

        Returns:
            Dict[str, any]: Diccionario con la información extraída por ffmpeg.
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
        Returns the raw format information of the video file.

        Returns:
            Dict: Raw format information of the video file.
        """
        return self._raw_data.get("format", {})
    
    def _get_raw_streams_info(self) -> List[Dict]:
        """
        Returns the raw streams information of the video file.

        Returns:
            List[Dict]: Raw streams information of the video file.
        """
        return self._raw_data.get("streams", [])
        
    def analyze(self) -> Optional[AudioFileSchema]:
        """
        Mapea la información cruda al esquema Pydantic.

        Returns:
            Optional[AudioFileSchema]: Objeto AudioFileSchema con la información del archivo analizado.
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
            "metadata": format_info.get("tags", {}) # Pydantic se encarga de filtrar los tags
        }

        try:
            return AudioFileSchema(**data_for_schema)
        except Exception as e:
            self.logger.error(f"Error validando datos con Pydantic: {e}")
            return None

    @property
    def raw_data(self):
        """
        Returns the raw data of the video file.

        Returns:
            Dict: Raw data of the video file.
        """
        return self._raw_data