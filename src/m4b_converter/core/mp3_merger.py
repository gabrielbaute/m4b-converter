import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
from typing import List, Optional, Dict, Callable

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
                [Path(root) / Path(file)  # Convertir `file` a Path
                for root, _, files in os.walk(self.input_path) 
                for file in files 
                if Path(file).suffix.lower() == '.mp3']
            )
            if not mp3_files:
                raise Exception(f"No se encontraron archivos MP3 en {self.input_path}")
            
            return mp3_files
        
        except Exception as e:
            raise Exception(f"Error al buscar MP3: {e}")

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

    def _build_command(self, tmp_path: Path, output_file: Path) -> list:
        return [
            "ffmpeg",
            "-hide_banner",  # Oculta información de copyright
            "-loglevel", "error",  # Solo muestra errores
            "-f", "concat",
            "-safe", "0",
            "-i", str(tmp_path),
            "-c", "copy",
            str(output_file)
        ]
    
    def merge(
        self,
        output_name: str = "merged.mp3",
        metadata: Optional[Dict[str, str]] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Path:
        """Fusiona MP3s en un solo archivo."""
        if not self.mp3_files:
            raise ValueError("No hay archivos MP3 para fusionar.")

        output_file = self.output_dir / output_name
        
        try:
            with NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp_file:
                tmp_path = Path(tmp_file.name)
                for mp3 in self.mp3_files:
                    tmp_file.write(f"file '{mp3.absolute()}'\n")

            command = self._build_command(tmp_path, output_file)
            
            # Ejecutar FFmpeg sin mostrar output
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                #stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                #stderr=subprocess.DEVNULL,
                universal_newlines=True
            )

            # Leer salida para progreso (adaptar según necesidad)
            for line in process.stdout:
                if progress_callback:
                    progress_callback(line.strip())

            if process.wait() != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            if metadata:
                self._add_metadata(output_file, metadata)

            if progress_callback:
                progress_callback("Fusión completada!")

            return output_file

        except subprocess.CalledProcessError as e:
            if output_file.exists():
                output_file.unlink()
            raise RuntimeError(f"Error al fusionar MP3s: {e}")
        finally:
            if tmp_path.exists():
                tmp_path.unlink()