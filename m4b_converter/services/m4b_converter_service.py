import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

from m4b_converter.settings import AppSettings
from m4b_converter.enums import Bitrate, AudioProfile
from m4b_converter.schemas import AudioFileSchema, ConversionTask, ConversionResult

class M4bConverterService:
    def __init__(
        self, 
        audio_info: AudioFileSchema,
        output_dir: Optional[Path] = AppSettings.OUTPUT_DIR
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.audio_info = audio_info
        self.output_dir = output_dir
        self.current_task: Optional[ConversionTask] = None

    def _build_ffmpeg_command(
        self,
        task: ConversionTask,
        output_path: Path,
        profile: AudioProfile,
        threads: int,
        cover_path: Optional[Path] = None
    ) -> list:
        """Construye el comando optimizado para audiolibros."""
        
        # Base: audio mapping
        cmd = [
            "ffmpeg", "-i", str(self.audio_info.path)
        ]

        # Si hay portada, la incluimos como segundo input
        if cover_path and cover_path.exists():
            cmd.extend(["-i", str(cover_path)])
            # Mapeamos audio del primer input y video del segundo
            cmd.extend(["-map", "0:a", "-map", "1:v"])
            # Configuramos el stream de video como 'attached_pic' para m4b
            cmd.extend(["-c:v", "copy", "-disposition:v", "attached_pic"])
        else:
            cmd.extend(["-vn"]) # No video si no hay portada

        # Parámetros de audio
        cmd.extend([
            "-c:a", "aac",
            "-b:a", task.bitrate_target,
            "-ac", str(task.channels_target),
            "-threads", str(threads),
            "-f", "mp4", # m4b es técnicamente un wrapper mp4
        ])

        # Inyectar metadatos desde nuestro schema
        meta = self.audio_info.metadata
        if meta.title: cmd.extend(["-metadata", f"title={meta.title}"])
        if meta.artist: cmd.extend(["-metadata", f"artist={meta.artist}"])
        if meta.album: cmd.extend(["-metadata", f"album={meta.album}"])

        cmd.append(str(output_path))
        return cmd

    def _parse_ffmpeg_time(self, line: str) -> float:
        """
        Extrae los segundos de una línea de progreso de FFmpeg.

        Args:
            line(str): Línea de progreso de FFmpeg.
        
        Returns:
            float: Segundos transcurridos.
        """
        try:
            # ffprobe time=00:00:00.00
            time_str = line.split("time=")[1].split()[0]
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        except:
            return 0.0

    def convert(
        self,
        bitrate: Bitrate = Bitrate.B_64K,
        channels: int = 1,
        cover_path: Optional[Path] = None,
        progress_callback: Optional[Callable[[float], None]] = None,
        task: Optional[ConversionTask] = None
    ) -> ConversionResult:
        
        # 1. Crear la tarea
        self.current_task = task or ConversionTask(
            input_path=self.audio_info.path,
            bitrate_target=bitrate.value,
            channels_target=channels
        )

        output_path = self.output_dir / f"{self.audio_info.path.stem}.m4b"
        temp_path = AppSettings.TEMP_DIR / f"{self.current_task.id}.m4b"

        cmd = self._build_ffmpeg_command(
            self.current_task, temp_path, AudioProfile.AAC_LOW, threads=0, cover_path=cover_path
        )

        self.logger.info(f"Iniciando conversión ID: {self.current_task.id}")

        try:
            # Definimos el tiempo de inicio de la tarea
            timestamp_start = datetime.now()
            
            # Ejecución con captura de progreso
            process = subprocess.Popen(
                cmd, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8"
            )

            for line in process.stderr:
                if progress_callback and "time=" in line:
                    # Cálculo de progreso simple basado en tiempo/duración total
                    current_time = self._parse_ffmpeg_time(line)
                    percent = (current_time / self.audio_info.duration_seconds) * 100
                    progress_callback(min(round(percent, 2), 99.9))

            if process.wait() != 0:
                raise RuntimeError("FFmpeg falló en la ejecución.")

            # 2. Finalizar y mover
            output_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path.replace(output_path)

            # 3. Retornar objeto de resultado
            return ConversionResult(
                task_id=self.current_task.id,
                output_path=output_path,
                duration_seconds=self.audio_info.duration_seconds,
                size_original_bytes=self.audio_info.size_bytes,
                size_final_bytes=output_path.stat().st_size,
                bitrate_final=bitrate.value,
                timestamp_start=timestamp_start,
                timestamp_end=datetime.now()
            )

        except Exception as e:
            if temp_path.exists(): temp_path.unlink()
            self.logger.error(f"Error en conversión {self.current_task.id}: {e}")
            raise