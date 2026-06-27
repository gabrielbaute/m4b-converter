from pathlib import Path

__version__ = "1.1.1"

class AppSettings:
    """
    Configuración de la aplicación M4B Converter.

    Esta clase maneja la configuración global de la aplicación, incluyendo el nombre, versión y estructura de directorios necesarios para el funcionamiento del conversor de audiolibros a formato M4B.

    Attributes:
        NAME (str): Nombre de la aplicación.
        VERSION (str): Versión actual de la aplicación.
        APP_DIR (Path): Directorio raíz de la aplicación en el home del usuario.
        TEMP_DIR (Path): Directorio para archivos temporales durante la conversión.
        OUTPUT_DIR (Path): Directorio donde se guardan los archivos M4B convertidos.
        LOGS_DIR (Path): Directorio para almacenar los archivos de registro (logs).
    """
    # Datos de la app
    NAME: str = "M4B Converter"
    VERSION: str = __version__

    # Directorios
    APP_DIR: Path = Path.home() / ".m4b_converter"
    TEMP_DIR: Path = APP_DIR / "temp"
    OUTPUT_DIR: Path = APP_DIR / "output"
    LOGS_DIR: Path = APP_DIR / "logs"

    # Crear directorios si no existen
    APP_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)