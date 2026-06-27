"""
Gestores y orquestadores del flujo de trabajo de conversión.

Este paquete contiene los orquestadores que coordinan los diferentes servicios para ejecutar el flujo completo de conversión de archivos de audio a M4B.
"""
from m4b_converter.managers.workflow_manager import WorkflowManager

__all__ = [
    "WorkflowManager"
]