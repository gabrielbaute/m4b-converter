from pathlib import Path

class AppSettings:
    """
    Configuración de la aplicación.
    """
    APP_DIR: Path = Path.home() / ".m4b_converter"
    TEMP_DIR: Path = APP_DIR / "temp"
    OUTPUT_DIR: Path = APP_DIR / "output"
    LOGS_DIR: Path = APP_DIR / "logs"

    # Crear directorios si no existen
    APP_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)