import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, List

from m4b_converter.settings import AppSettings
from m4b_converter.enums import Bitrate, AudioProfile
from m4b_converter.schemas import AudioFileSchema, ConversionTask, ConversionResult


class M4bConverterService:
    """
    Servicio principal para la conversión de archivos de audio a formato M4B.

    Esta clase orquesta el proceso de conversión utilizando ffmpeg, manejando la construcción de comandos, la ejecución con seguimiento de progreso, y la gestión de archivos temporales. Está optimizada específicamente para la conversión de audiolibros, incluyendo soporte para portadas, metadatos y configuración de calidad.

    El servicio trabaja en conjunto con AudioAnalyzerService y ExtractCoverService para proporcionar un flujo completo de conversión.

    Attributes:
        audio_info (AudioFileSchema): Información estructurada del archivo de audio obtenida mediante AudioAnalyzerService.
        output_dir (Path): Directorio donde se guardará el archivo convertido.
        logger (logging.Logger): Logger para registrar eventos y errores.
        current_task (Optional[ConversionTask]): Tarea de conversión actual en ejecución.

    Example:
        >>> from pathlib import Path
        >>> from m4b_converter.services import AudioAnalyzerService, M4bConverterService
        >>> from m4b_converter.enums import Bitrate
        >>>
        >>> # Analizar el archivo primero
        >>> analyzer = AudioAnalyzerService(Path("audiolibro.mp3"))
        >>> audio_info = analyzer.analyze()
        >>>
        >>> # Convertir a M4B
        >>> converter = M4bConverterService(audio_info)
        >>> result = converter.convert(
        ...     bitrate=Bitrate.B_64K,
        ...     channels=1,
        ...     cover_path=Path("portada.jpg")
        ... )
        >>> print(f"Archivo convertido: {result.output_path}")
    """

    def __init__(
        self, 
        audio_info: AudioFileSchema,
        output_dir: Optional[Path] = AppSettings.OUTPUT_DIR
    ):
        """
        Inicializa el servicio de conversión a M4B.

        Args:
            audio_info (AudioFileSchema): Información del archivo de audio a convertir, obtenida mediante AudioAnalyzerService. Contiene metadatos, duración, bitrate y demás características técnicas.
            output_dir (Optional[Path]): Directorio donde se guardará el archivo convertido. Por defecto usa AppSettings.OUTPUT_DIR.
        """
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
    ) -> List[str]:
        """
        Construye el comando ffmpeg para la conversión optimizada a audiolibros.

        Este método genera el comando completo de ffmpeg incluyendo:
        - Mapeo de audio y video (portada)
        - Configuración de codec AAC con perfil y bitrate específicos
        - Inyección de metadatos (título, artista, álbum)
        - Configuración de canales y threads

        Args:
            task (ConversionTask): Tarea de conversión que contiene los parámetros de destino (bitrate, canales).
            output_path (Path): Ruta donde se guardará el archivo temporal.
            profile (AudioProfile): Perfil de audio AAC a utilizar.
            threads (int): Número de hilos para la codificación (0 = auto).
            cover_path (Optional[Path]): Ruta a la imagen de portada a incrustar. Si se proporciona y existe, se incluye como attached_pic.

        Returns:
            List[str]: Lista con el comando ffmpeg y sus argumentos, listo para
                ser ejecutado con subprocess.

        Note:
            - Si se incluye portada, se usa el segundo input y se mapea como 'attached_pic' para compatibilidad con M4B.
            - El formato de salida es MP4 (que es el contenedor de M4B).
        """
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
            cmd.extend(["-vn"])  # No video si no hay portada

        # Parámetros de audio
        cmd.extend([
            "-c:a", "aac",
            "-b:a", task.bitrate_target,
            "-ac", str(task.channels_target),
            "-threads", str(threads),
            "-f", "mp4",  # m4b es técnicamente un wrapper mp4
        ])

        # Inyectar metadatos desde nuestro schema
        meta = self.audio_info.metadata
        if meta.title:
            cmd.extend(["-metadata", f"title={meta.title}"])
        if meta.artist:
            cmd.extend(["-metadata", f"artist={meta.artist}"])
        if meta.album:
            cmd.extend(["-metadata", f"album={meta.album}"])

        cmd.append(str(output_path))
        return cmd

    def _parse_ffmpeg_time(self, line: str) -> float:
        """
        Extrae los segundos transcurridos de una línea de progreso de FFmpeg.

        Este método analiza la salida de ffmpeg para extraer el tiempo actual de procesamiento, que se utiliza para calcular el porcentaje de progreso durante la conversión.

        Args:
            line (str): Línea de salida de ffmpeg que contiene "time=".

        Returns:
            float: Segundos transcurridos del procesamiento. Retorna 0.0 si no se puede parsear el tiempo.

        Example:
            >>> line = "frame=1234 time=00:15:30.45 bitrate=128k"
            >>> converter._parse_ffmpeg_time(line)
            930.45
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
        """
        Ejecuta la conversión del archivo de audio a formato M4B.

        Este método realiza el proceso completo de conversión:
        1. Crea o recibe una tarea de conversión con los parámetros especificados
        2. Genera el comando ffmpeg con todos los parámetros optimizados
        3. Ejecuta la conversión con seguimiento de progreso en tiempo real
        4. Mueve el archivo temporal al directorio de salida
        5. Retorna un objeto ConversionResult con todas las métricas

        Args:
            bitrate (Bitrate): Bitrate objetivo para el archivo convertido. Por defecto Bitrate.B_64K (64 kbps), óptimo para voz.
            channels (int): Número de canales de audio (1=mono, 2=estéreo). Por defecto 1 (mono), recomendado para audiolibros.
            cover_path (Optional[Path]): Ruta a la imagen de portada a incrustar. Si se proporciona, se incluye como attached_pic en el M4B.
            progress_callback (Optional[Callable[[float], None]]): Función callbackque recibe el porcentaje de progreso (0-100) durante la conversión. Útil para interfaces de usuario o barras de progreso.
            task (Optional[ConversionTask]): Tarea de conversión preconfigurada. Si no se proporciona, se crea una nueva con los parámetros dados.

        Returns:
            ConversionResult: Objeto con todas las métricas y resultados de la conversión, incluyendo IDs, tiempos, tamaños y rutas.

        Raises:
            RuntimeError: Si ffmpeg falla durante la ejecución.
            Exception: Cualquier otro error durante la conversión (se maneja limpiando archivos temporales antes de relanzar).

        Example:
            >>> from m4b_converter.services import M4bConverterService
            >>> from m4b_converter.enums import Bitrate
            >>>
            >>> # Función para mostrar progreso
            >>> def mostrar_progreso(pct):
            ...     print(f"Progreso: {pct:.1f}%")
            >>>
            >>> # Convertir con portada y callback
            >>> result = converter.convert(
            ...     bitrate=Bitrate.B_96K,
            ...     channels=2,
            ...     cover_path=Path("portada.jpg"),
            ...     progress_callback=mostrar_progreso
            ... )
            >>>
            >>> # Acceder a los resultados
            >>> print(f"Tamaño original: {result.size_original_bytes} bytes")
            >>> print(f"Tamaño final: {result.size_final_bytes} bytes")
            >>> print(f"Compresión: {result.compression_ratio*100:.1f}%")

        Note:
            - La conversión se realiza primero en un archivo temporal en AppSettings.TEMP_DIR para evitar archivos corruptos en caso de error.
            - Si el proceso falla, se limpia automáticamente el archivo temporal.
            - El progreso se calcula comparando el tiempo procesado con la duración total del archivo (máximo 99.9% hasta finalizar).
        """
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
            if temp_path.exists():
                temp_path.unlink()
            self.logger.error(f"Error en conversión {self.current_task.id}: {e}")
            raise