import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Callable

class Mp3Merger:
    def __init__(self, input_path: str, output_dir: str = "output", temp_dir: str = "temp"):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)

        # Crear directorios si no existen
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

        self.output_filename = "merged.mp3"
        self.output_path = self.output_dir / self.output_filename
        self.temp_list_path = self.temp_dir / "mp3_list.txt"

        self.mp3_files = self._collect_mp3_files()

    def _collect_mp3_files(self) -> List[Path]:
        """Recoge archivos MP3 recursivamente, ordenados por nombre."""
        try:
            mp3_files = sorted(
                [Path(root) / Path(file) 
                 for root, _, files in os.walk(self.input_path) 
                 for file in files 
                 if file.lower().endswith('.mp3')]
            )
            if not mp3_files:
                raise Exception(f"No se encontraron archivos MP3 en {self.input_path}")
            
            return mp3_files
        
        except Exception as e:
            raise Exception(f"Error al buscar MP3: {e}")

    def _build_ffmpeg_command(self) -> list:
        return [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-f", "concat",
            "-safe", "0",
            "-i", str(self.temp_list_path.absolute()),
            "-c", "copy",
            str(self.output_path)
        ]

    def merge(
        self,
        metadata: Optional[Dict[str, str]] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Path:
        """Fusiona MP3s en un solo archivo y opcionalmente añade metadatos."""
        if not self.mp3_files:
            raise ValueError("No hay archivos MP3 para fusionar.")

        try:
            # Crear archivo temporal con la lista de archivos
            with open(self.temp_list_path, "w") as temp_file:
                for mp3 in self.mp3_files:
                    temp_file.write(f"file {mp3.absolute().as_posix()}\n")
                    
            
            if not self.temp_list_path.exists():
                raise RuntimeError("El archivo de lista de MP3 no fue generado correctamente.")
            
            with open(self.temp_list_path, "r") as temp_file:
                print("Contenido del archivo de concatenación:")
                print(temp_file.read())

            command = self._build_ffmpeg_command()

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            print("Salida de FFmpeg:")
            print(stdout)
            print("Errores de FFmpeg:")
            print(stderr)

            if process.returncode != 0:
                raise RuntimeError(f"Error al fusionar MP3s:\n{stderr}")

            
            for line in process.stdout:
                if progress_callback:
                    progress_callback(line.strip())

            if process.wait() != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            # **Agregar metadatos después de la fusión**
            if metadata:
                self._add_metadata(self.output_path, metadata)

            if progress_callback:
                progress_callback("Fusión completada!")

            return self.output_path

        except subprocess.CalledProcessError as e:
            if self.output_path.exists():
                self.output_path.unlink()
            raise RuntimeError(f"Error al fusionar MP3s: {e}")

        finally:
            if self.temp_list_path.exists():
                self.temp_list_path.unlink()