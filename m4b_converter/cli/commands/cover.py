"""
Extract cover mmand for audio files.
"""
from pathlib import Path
from rich.table import Table
from rich.console import Console

from m4b_converter.services import ExtractCoverService, AudioAnalyzerService

def handle_cover(file_path: Path, console: Console) -> None:
    """
    Extrae la imagen incrustada del archivo de audio.
    
    Args:
        file_path(Path): Path to audiofile
        console(Console): Console object
    """
    analyer = AudioAnalyzerService(file_path=file_path)
    service = ExtractCoverService(file_path=file_path)
    cover_path = service.extract_cover(analyer.raw_data, output_dir=file_path.parent)

    if not cover_path:
        console.print(f"[red]Error:[/red] No se pudo extraer la portada: {file_path}")
        return

    console.print(f"[green]Portada extraída:[/green] {cover_path}")
    return cover_path