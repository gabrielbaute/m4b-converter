import logging
from pathlib import Path
from typing import Dict, Optional

from m4b_converter.settings.app_settings import AppSettings

class M4bLogger:
    """
    Configuración del sistema de logs.
    """
    LOG_FILE: Path = AppSettings.LOGS_DIR / "app.log"
    LEVEL_MAP: Dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    @staticmethod
    def setup_logging(level: Optional[str] = "INFO") -> None:
        """
        Configura el sistema de logging básico.

        Args:
            level (Optional[str]): Nivel de registro. Ejemplo: "DEBUG", "INFO", etc.

        Returns:
            None
        """
        AppSettings.LOGS_DIR.mkdir(parents=True, exist_ok=True)

        if not M4bLogger.LOG_FILE.exists():
            M4bLogger.LOG_FILE.touch()
        
        logging.basicConfig(
            level=M4bLogger.LEVEL_MAP.get(level, logging.INFO),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(M4bLogger.LOG_FILE, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
