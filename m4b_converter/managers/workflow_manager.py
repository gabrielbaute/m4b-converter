import uuid
import shutil
import logging
from pathlib import Path
from typing import Optional, Callable, List

from m4b_converter.services import AudioAnalyzerService, ExtractCoverService, M4bConverterService
from m4b_converter.schemas import ConversionResult, ConversionTask
from m4b_converter.enums import Bitrate, Format
from m4b_converter.settings import AppSettings


class WorkflowManager:
    """
    Orquestador central que gestiona el ciclo de vida completo de la conversión.

    Esta clase coordina todos los servicios necesarios para convertir un archivo de audio a formato M4B, ejecutando el flujo completo en el orden correcto:

    1. Análisis del archivo de audio (AudioAnalyzerService)
    2. Extracción de la portada si existe (ExtractCoverService)
    3. Conversión a M4B con parámetros optimizados (M4bConverterService)
    4. Persistencia de la portada y limpieza de archivos temporales

    El WorkflowManager actúa como fachada (Facade Pattern) simplificando la interacción con los servicios subyacentes y manejando la orquestación de todas las operaciones.

    Attributes:
        logger (logging.Logger): Logger para registrar eventos y errores durante todo el flujo de trabajo.

    Example:
        >>> from pathlib import Path
        >>> from m4b_converter.managers import WorkflowManager
        >>> from m4b_converter.enums import Bitrate
        >>>
        >>> manager = WorkflowManager()
        >>>
        >>> # Procesar un solo archivo
        >>> result = manager.process_file(
        ...     input_path=Path("audiolibro.mp3"),
        ...     bitrate=Bitrate.B_64K,
        ...     channels=1
        ... )
        >>>
        >>> if result:
        ...     print(f"✅ Conversión exitosa: {result.output_path}")
        ...     print(f"📊 Compresión: {result.compression_ratio*100:.1f}%")
        >>>
        >>> # Procesar directorio completo
        >>> results = manager.process_directory(
        ...     input_dir=Path("./audiolibros/"),
        ...     recursive=True
        ... )
        >>> print(f"✅ {len(results)} archivos convertidos")
    """

    def __init__(self):
        """
        Inicializa el orquestador de flujo de trabajo.

        Configura el logger para el seguimiento de todas las operaciones durante el proceso de conversión.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_file(
        self, 
        input_path: Path, 
        bitrate: Bitrate = Bitrate.B_64K,
        channels: int = 1,
        output_dir: Optional[Path] = AppSettings.OUTPUT_DIR,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> Optional[ConversionResult]:
        """
        Ejecuta el flujo completo de conversión para un solo archivo.

        Este método orquesta todas las etapas del proceso:
        - Análisis del archivo para obtener información técnica y metadatos
        - Extracción de la portada (si existe en el archivo)
        - Conversión a M4B con los parámetros especificados
        - Persistencia de la portada en el directorio de salida
        - Limpieza de archivos temporales

        Args:
            input_path (Path): Ruta del archivo de audio a procesar. Debe ser un archivo existente y accesible.
            bitrate (Bitrate): Bitrate objetivo para el archivo de salida. Por defecto Bitrate.B_64K (64 kbps), óptimo para voz.
            channels (int): Número de canales de audio (1=mono, 2=estéreo). Por defecto 1 (mono), recomendado para audiolibros.
            output_dir (Optional[Path]): Directorio donde se guardará el archivo convertido. Por defecto usa AppSettings.OUTPUT_DIR.
            progress_callback (Optional[Callable[[float], None]]): Función callback que recibe el porcentaje de progreso (0-100) durante la conversión. Útil para interfaces de usuario.

        Returns:
            Optional[ConversionResult]: Objeto con los resultados y métricas de la conversión. Retorna None si:
                - El archivo no pudo ser analizado correctamente.
                - Ocurre un error durante cualquier etapa del proceso.

        Raises:
            Exception: Cualquier error no manejado durante el proceso (se captura y se registra antes de retornar None).

        Example:
            >>> from m4b_converter.managers import WorkflowManager
            >>> from m4b_converter.enums import Bitrate
            >>>
            >>> manager = WorkflowManager()
            >>>
            >>> # Conversión básica
            >>> result = manager.process_file(
            ...     input_path=Path("mi_audio.mp3"),
            ...     bitrate=Bitrate.B_96K
            ... )
            >>>
            >>> # Conversión con callback de progreso
            >>> def mostrar_progreso(pct):
            ...     print(f"Progreso: {pct:.1f}%")
            >>>
            >>> result = manager.process_file(
            ...     input_path=Path("mi_audio.mp3"),
            ...     bitrate=Bitrate.B_128K,
            ...     channels=2,
            ...     progress_callback=mostrar_progreso
            ... )

        Note:
            - La portada extraída se guarda como JPG en el mismo directorio que el archivo convertido, con el nombre "{input_path.stem}.jpg"
            - Los archivos temporales de portada se eliminan automáticamente después de copiarlos al destino final.
            - El método maneja todas las excepciones internamente y retorna None en caso de error, registrando el problema en el log.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        # 0. Creamos la tarea aquí (El "Ticket" de seguimiento)
        task = ConversionTask(
            id=uuid.uuid4(),
            input_path=input_path,
            bitrate_target=bitrate.value,
            channels_target=channels
        )
        
        self.logger.info(f"--- [TASK {task.id}] Procesando: {input_path.name} ---")
        
        try:
            # 1. Analizar el archivo
            analyzer = AudioAnalyzerService(input_path)
            audio_info = analyzer.analyze()
            
            if not audio_info:
                self.logger.error(f"No se pudo analizar el archivo: {input_path}")
                return None

            # 2. Extraer portada (si existe)
            # Usamos el raw_data guardado en el analyzer
            extractor = ExtractCoverService(input_path)
            temp_cover_path = extractor.extract_cover(analyzer.raw_data, output_dir=AppSettings.TEMP_DIR)
            
            if temp_cover_path:
                self.logger.info(f"Portada extraída en: {temp_cover_path}")

            # 3. Convertir
            converter = M4bConverterService(audio_info, output_dir=output_dir)
            result = converter.convert(
                bitrate=bitrate,
                channels=channels,
                cover_path=temp_cover_path,
                progress_callback=progress_callback,
                task=task
            )

            # 4. Persistencia y Limpieza de Portada
            if temp_cover_path and temp_cover_path.exists():
                # Definimos la ruta final de la imagen en el output_dir
                final_cover_path = output_dir / f"{input_path.stem}.jpg"
                
                # Movemos/Copiamos la imagen al destino final
                shutil.copy2(temp_cover_path, final_cover_path)
                self.logger.info(f"Portada guardada en: {final_cover_path}")
                
                # Ahora sí, limpiamos el temporal
                temp_cover_path.unlink()
                self.logger.debug("Limpieza de temporal de portada completada.")

            self.logger.info(
                f"Éxito: {result.output_path.name} | "
                f"Reducción: {result.compression_ratio * 100}%"
            )
            
            return result

        except Exception as e:
            self.logger.critical(f"Error en workflow para {input_path.name}: {e}")
            return None
        
    def process_directory(
        self,
        input_dir: Path,
        bitrate: Bitrate = Bitrate.B_64K,
        channels: int = 1,
        recursive: bool = False,
        output_dir: Optional[Path] = AppSettings.OUTPUT_DIR,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[ConversionResult]:
        """
        Escanea un directorio y procesa todos los archivos de audio compatibles.

        Este método busca automáticamente todos los archivos de audio con extensiones compatibles (MP3, M4A, WAV, FLAC, OPUS, OGG) en el directorio especificado y los convierte uno por uno.

        Args:
            input_dir (Path): Directorio que contiene los archivos de audioa procesar. Debe existir y ser accesible.
            bitrate (Bitrate): Bitrate objetivo para todos los archivos convertidos. Por defecto Bitrate.B_64K.
            channels (int): Número de canales para todos los archivos convertidos (1=mono, 2=estéreo). Por defecto 1.
            recursive (bool): Si es True, busca archivos recursivamente en subdirectorios. Por defecto False (solo nivel superior).
            output_dir (Optional[Path]): Directorio donde se guardarán los archivos convertidos. Por defecto usa AppSettings.OUTPUT_DIR.
            progress_callback (Optional[Callable[[float], None]]): Función callback para el progreso global del proceso por lotes.

        Returns:
            List[ConversionResult]: Lista de objetos ConversionResult para cada archivo procesado exitosamente. Los archivos que fallaron no se incluyen en la lista.

        Example:
            >>> from m4b_converter.managers import WorkflowManager
            >>> from pathlib import Path
            >>>
            >>> manager = WorkflowManager()
            >>>
            >>> # Procesar todos los MP3 en un directorio
            >>> results = manager.process_directory(
            ...     input_dir=Path("./audiolibros/"),
            ...     bitrate=Bitrate.B_64K,
            ...     channels=1,
            ...     recursive=True
            ... )
            >>>
            >>> print(f"✅ {len(results)} archivos convertidos")
            >>> for r in results:
            ...     print(f"  - {r.output_path.name} ({r.compression_ratio*100:.1f}%)")

        Note:
            - Solo se procesan archivos con extensiones definidas en el enum Format (excluyendo M4B para evitar reconversiones innecesarias).
            - Las extensiones se verifican en minúsculas para mayor flexibilidad.
            - Si no se encuentra ningún archivo compatible, retorna una lista vacía.
            - El callback de progreso se pasa a cada conversión individual, pero no se utiliza para el progreso global del lote.
        """
        self.logger.info(f"Escaneando directorio: {input_dir}")
        
        # Extensiones válidas basadas en tu Enum Format
        valid_extensions = {f".{fmt.value}" for fmt in Format if fmt != Format.M4B}
        
        # Búsqueda de archivos
        search_pattern = "**/*" if recursive else "*"
        files_to_process = [
            f for f in input_dir.glob(search_pattern) 
            if f.suffix.lower() in valid_extensions
        ]

        if not files_to_process:
            self.logger.warning(f"No se encontraron archivos compatibles en {input_dir}")
            return []

        self.logger.info(f"Se han encontrado {len(files_to_process)} archivos para procesar.")
        
        results: List[ConversionResult] = []

        for index, file_path in enumerate(files_to_process, 1):
            self.logger.info(f"Procesando [{index}/{len(files_to_process)}]: {file_path.name}")
            
            # Aquí podrías inyectar un callback de progreso que informe qué archivo está procesando
            result = self.process_file(
                input_path=file_path,
                bitrate=bitrate,
                channels=channels,
                output_dir=output_dir,
                progress_callback=progress_callback
            )
            
            if result:
                results.append(result)
            else:
                self.logger.error(f"Fallo al procesar: {file_path.name}")

        return results