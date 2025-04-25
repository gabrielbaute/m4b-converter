import os
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
from typing import List, Optional

logging.basicConfig(level=logging.INFO)

class Mp3Merger:
    def __init__(self, input_path: str, temp_dir: str = "temp"):
        self.input_path = Path(input_path)
        self.temp_dir = Path(temp_dir)
        
        if not self.input_path.exists() or not self.input_path.is_dir():
            raise ValueError(f"Directorio inválido: {input_path}")
        
        self.temp_dir.mkdir(exist_ok=True)
        self.mp3_files = self._collect_mp3_files()

    def _collect_mp3_files(self) -> List[Path]:
        """Recoge archivos MP3 recursivamente, ordenados por nombre."""
        try:
            mp3_files = sorted(
                [Path(root) / file 
                 for root, _, files in os.walk(self.input_path) 
                 for file in files 
                 if file.suffix.lower() == '.mp3']
            )
            if not mp3_files:
                logging.warning(f"No se encontraron archivos MP3 en {self.input_path}")
            return mp3_files
        except Exception as e:
            logging.error(f"Error al buscar MP3: {e}")
            raise

    def merge(self, output_name: str = "merged.mp3") -> Optional[Path]:
        """Fusiona MP3s en un solo archivo usando FFmpeg.
        
        Returns:
            Path: Ruta del archivo fusionado o None si falla.
        """
        if not self.mp3_files:
            return None

        output_file = self.temp_dir / output_name
        
        try:
            with NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)
                for mp3 in self.mp3_files:
                    tmp_file.write(f"file '{mp3.absolute()}'\n")

            subprocess.run([
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(tmp_path),
                "-c", "copy",
                str(output_file)
            ], check=True)

            logging.info(f"Archivos fusionados en {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg falló: {e}")
            if output_file.exists():
                output_file.unlink()
            return None
        finally:
            if tmp_path.exists():
                tmp_path.unlink()