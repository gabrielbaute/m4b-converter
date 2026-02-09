import shutil
import logging
from pathlib import Path
from typing import Optional, Callable, List, Dict

from m4b_converter.services import AudioAnalyzerService, ExtractCoverService, M4bConverterService
from m4b_converter.schemas import ConversionResult
from m4b_converter.enums import Bitrate, Format
from m4b_converter.settings import AppSettings

class WorkflowManager:
    """
    Orquestador central que gestiona el ciclo de vida completo de la conversión.
    """
    def __init__(self):
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
        Ejecuta el flujo completo: Análisis -> Extracción de Portada -> Conversión -> Limpieza.

        Args:
            input_path(Path): Ruta del archivo de audio a procesar.
            bitrate(Bitrate): Bitrate del archivo de salida. 64K por defecto.
            channels(int): Canales del archivo de salida. 1 por defecto.
            output_dir(Optional[Path]): Directorio de salida para el archivo convertido.
            progress_callback(Optional[Callable[[float], None]]): Callback de progreso.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"--- Iniciando procesamiento: {input_path.name} ---")
        
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
                progress_callback=progress_callback
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