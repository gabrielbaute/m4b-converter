import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Callable

class M4bConverter:
    def __init__(
        self,
        input_path: str,
        output_dir: str = "output",
        temp_dir: str = "temp",
        metadata: Optional[Dict[str, str]] = None
    ):
        self.input_path = Path(input_path)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        self.metadata = metadata or {
            "title": "Audiolibro",
            "artist": "Autor",
            "genre": "Audiolibro"
        }

        # Crear directorios si no existen
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

        # Generar nombres de archivos
        self.output_filename = self._generate_output_filename()
        self.output_path = self.output_dir / self.output_filename
        self.temp_path = self.temp_dir / self.output_filename

    def _generate_output_filename(self) -> str:
        """Genera el nombre del archivo de salida basado en el input."""
        return f"{self.input_path.stem}.m4b"

    def _build_ffmpeg_command(
        self,
        output_path: Path,
        bitrate: str = "64k",
        audio_profile: str = "aac_low",
        channels: int = 1,
        threads: int = 1
    ) -> list:
        """Construye el comando FFmpeg base."""
        command = [
            "ffmpeg",
            "-i", str(self.input_path),
            "-threads", str(threads),
            "-c:a", "aac",
            "-profile:a", audio_profile,
            "-b:a", bitrate,
            "-ac", str(channels),
            "-f", "mp4",
            "-vn"
        ]

        # Añadir metadatos
        for key, value in self.metadata.items():
            command.extend(["-metadata", f"{key}={value}"])

        command.append(str(output_path))
        return command

    def _move_to_output(self, temp_path: Path) -> None:
        """Mueve el archivo temporal al directorio final."""
        if temp_path.exists():
            shutil.move(str(temp_path), str(self.output_path))

    def convert_to_m4b(
        self,
        bitrate: str = "64k",
        channels: int = 1,
        threads: int = 1,
        progress_callback: Optional[Callable] = None,
        remove_temp: bool = True
    ) -> Path:
        """
        Convierte el archivo a M4B.
        
        Args:
            progress_callback: Función para reportar progreso (ej: lambda p: print(f"{p}%")).
        """
        try:
            # Paso 1: Convertir a archivo temporal
            command = self._build_ffmpeg_command(
                output_path=self.temp_path,
                bitrate=bitrate,
                channels=channels,
                threads=threads
            )

            process = subprocess.Popen(
                command,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stderr:
                if progress_callback and "time=" in line:
                    time_str = line.split("time=")[1].split()[0]
                    progress_callback(time_str)

            if process.wait() != 0:
                raise subprocess.CalledProcessError(process.returncode, command)

            # Paso 2: Mover a output_dir
            self._move_to_output(self.temp_path)

            return self.output_path

        except Exception as e:
            if self.temp_path.exists():
                self.temp_path.unlink()  # Limpiar temporal en caso de error
            raise RuntimeError(f"Error al convertir a M4B: {e}")

        finally:
            if remove_temp and self.temp_path.exists():
                self.temp_path.unlink()  # Limpieza final

    def optimize_m4b(
        self,
        bitrate: str = "64k",
        channels: int = 1,
        threads: int = 1,
        progress_callback: Optional[Callable] = None
    ) -> Path:
        """Optimiza un archivo M4B existente."""
        return self.convert_to_m4b(
            bitrate=bitrate,
            channels=channels,
            threads=threads,
            progress_callback=progress_callback
        )