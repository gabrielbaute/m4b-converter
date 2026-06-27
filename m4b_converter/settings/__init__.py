"""
Configuración global de la aplicación.

Este paquete maneja la configuración de la aplicación incluyendo directorios, variables de entorno, versión y sistema de logging.
"""
from m4b_converter.settings.app_settings import AppSettings, __version__
from m4b_converter.settings.log_settings import M4bLogger

__all__ = [
    "AppSettings",
    "M4bLogger",
    "__version__"
]