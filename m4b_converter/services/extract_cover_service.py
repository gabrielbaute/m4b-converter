import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

class ExtractCoverService:
    """
    Servicio para extraer la imagen de portada (cover art) de archivos de audio.

    Esta clase proporciona funcionalidades para detectar y extraer imágenes incrustadas en archivos de audio, comúnmente utilizadas como portadas de audiolibros o álbumes musicales.

    El servicio utiliza ffmpeg para extraer la imagen del stream de video (attached_pic) y la guarda en formato JPEG en el directorio especificado.

    Attributes:
        file_path (Path): Ruta al archivo de audio del cual extraer la portada.
        logger (logging.Logger): Logger para registrar eventos y errores.

    Example:
        >>> from pathlib import Path
        >>> from m4b_converter.services import AudioAnalyzerService, ExtractCoverService
        >>>
        >>> audio_path = Path("mi_audiolibro.mp3")
        >>> analyzer = AudioAnalyzerService(audio_path)
        >>> raw_data = analyzer.raw_data
        >>>
        >>> extractor = ExtractCoverService(audio_path)
        >>> cover_path = extractor.extract_cover(raw_data)
        >>> if cover_path:
        ...     print(f"Portada extraída en: {cover_path}")
        ... else:
        ...     print("El archivo no contiene portada")
    """

    def __init__(self, file_path: Path):
        """
        Inicializa el servicio de extracción de portada.

        Args:
            file_path (Path): Ruta al archivo de audio que contiene la portada. El archivo debe existir y ser accesible.

        Raises:
            FileNotFoundError: Si el archivo no existe en la ruta especificada.
        """
        self.file_path = file_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def extract_cover(self, raw_data: Dict[str, Any], output_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Extrae la imagen incrustada del archivo de audio.

        Este método verifica la presencia de un stream de video con disposición 'attached_pic' (característico de portadas en archivos de audio) y extrae la imagen utilizando ffmpeg.

        Args:
            raw_data (Dict[str, Any]): Diccionario con la información cruda del archivo obtenida mediante ffprobe (usualmente de AudioAnalyzerService.raw_data). Contiene la sección 'streams' necesaria para detectar la presencia de la portada.
            output_dir (Optional[Path]): Directorio donde se guardará la imagen extraída. Si no se especifica, la imagen se guarda en el mismo directorio que el archivo de origen.

        Returns:
            Optional[Path]: Ruta al archivo de imagen extraído en formato JPEG. Retorna None si:
                - El archivo no contiene una portada incrustada.
                - Ocurre un error durante la extracción.

        Note:
            - La imagen se guarda con el nombre del archivo original seguido de "_cover.jpg" (ej: "mi_audiolibro_cover.jpg").
            - El formato de salida es siempre JPEG.
            - Se utiliza el flag "-y" en ffmpeg para sobrescribir si ya existe un archivo con el mismo nombre.

        Example:
            >>> from pathlib import Path
            >>> from m4b_converter.services import AudioAnalyzerService, ExtractCoverService
            >>>
            >>> # Análisis previo para obtener raw_data
            >>> analyzer = AudioAnalyzerService(Path("libro.mp3"))
            >>> raw = analyzer.raw_data
            >>>
            >>> # Extraer portada
            >>> extractor = ExtractCoverService(Path("libro.mp3"))
            >>> cover = extractor.extract_cover(raw, Path("./covers"))
            >>> 
            >>> # Verificar resultado
            >>> if cover and cover.exists():
            ...     print(f"Portada guardada en: {cover}")
            ... else:
            ...     print("No se encontró portada en el archivo.")
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