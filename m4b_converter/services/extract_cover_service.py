import logging
import subprocess
from typing import Optional, Dict
from pathlib import Path

class ExtractCoverService:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def extract_cover(self, raw_data: Dict[str, any], output_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Extrae la imagen incrustada del archivo de audio.

        Args:
            raw_data(Dict[str,any]): Diccionario con la información extraída por ffmpeg
            output_dir(Optional[Path]): Directorio de salida para la imagen. Si no se suministra, se coloca junto al archivo de origen.
        
        Returns:
            Optional[Path]: Ruta de la imagen extraída.
        """
        if not output_dir:
            output_dir = self.file_path.parent
        
        output_path = output_dir / f"{self.file_path.stem}_cover.jpg"
        
        # Comando: selecciona el stream de video (portada) y lo copia tal cual
        cmd = [
            "ffmpeg", "-i", str(self.file_path),
            "-an", "-vcodec", "copy",
            str(output_path), "-y"
        ]
        
        try:
            # Solo ejecutamos si detectamos que hay un attached_pic en el análisis previo
            streams = raw_data.get("streams", [])
            if any(s.get("disposition", {}).get("attached_pic") for s in streams):
                subprocess.run(cmd, capture_output=True, check=True)
                return output_path
        except subprocess.CalledProcessError:
            self.logger.error("No se pudo extraer la portada.")
        
        return None