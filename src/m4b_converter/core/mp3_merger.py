import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
from typing import List, Optional, Dict

class Mp3Merger:
    def __init__(self, input_path: str, output_dir: str = "output", temp_dir: str = "temp"):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        
        # Verifica si el directorio de entrada es válido o existe
        if not self.input_path.exists() or not self.input_path.is_dir():
            raise ValueError(f"Directorio inválido: {input_path}")
        
        # Crear directorios si no existen
        self.output_dir.mkdir(exist_ok=True)
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
                raise {f"No se encontraron archivos MP3 en {self.input_path}"}
            return mp3_files
        
        except Exception as e:
            raise {f"Error al buscar MP3: {e}"}

    def _add_metadata(self, file_path: Path, metadata: Dict[str, str]):
        """Añade metadatos al archivo usando FFmpeg."""
        metadata_args = []
        for key, value in metadata.items():
            metadata_args.extend(["-metadata", f"{key}={value}"])
        
        subprocess.run([
            "ffmpeg",
            "-i", str(file_path),
            *metadata_args,
            "-c", "copy",
            str(file_path.with_suffix(".temp.m4b"))  # Archivo temporal
        ], check=True)
        
        # Reemplazar el original
        file_path.with_suffix(".temp.m4b").replace(file_path)

    def merge(self, output_name: str = "merged.mp3", metadata: Optional[Dict[str, str]] = None) -> Optional[Path]:
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
            
            if metadata:
                self._add_metadata(output_file, metadata)
            
            print(f"Archivos fusionados en {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg falló: {e}")
            if output_file.exists():
                output_file.unlink()
            return None
        
        finally:
            if tmp_path.exists():
                tmp_path.unlink()