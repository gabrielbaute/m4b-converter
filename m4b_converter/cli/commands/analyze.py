"""
Analyze command for audio files.
"""
from pathlib import Path
from rich.table import Table
from rich.console import Console

from m4b_converter.services import AudioAnalyzerService
from m4b_converter.schemas import AudioFileSchema, AudioMetadata
from m4b_converter.cli.utils import convert_bytes_to_mb, parse_seconds

def analyze_audiobook(file_path: Path, console: Console) -> None:
    """
    Analyze an audiobook file.
    
    Args:
        file_path(Path): Path to audiofile
        console(Console): Console object
    """
    service = AudioAnalyzerService(file_path=file_path)
    info: AudioFileSchema = service.analyze()

    if not info:
        console.print(f"[red]Error:[/red] El archivo no se pudo analizar: {file_path}")
        return

    metadata: AudioMetadata = info.metadata
    size_mb = convert_bytes_to_mb(info.size_bytes)
    duration = parse_seconds(info.duration_seconds)

    table = Table(title=f"[bold magenta]Análisis de archivo[/bold magenta]: {metadata.title}", border_style="blue")
    table.add_column("Atributo", style="cyan", justify="right")
    table.add_column("Valor", style="green")

    table.add_row("Tamaño", f"{size_mb:.2f} MB")
    table.add_row("Duración", duration)
    table.add_row("Formato", info.format_name.value)
    table.add_row("Codec", info.codec)
    table.add_row("Bitrate", f"{info.bitrate_kbps} kbps")
    table.add_row("Frecuencia de muestreo", f"{info.sample_rate} Hz")
    table.add_row("Canales", f"{info.channels}")

    console.print(table)