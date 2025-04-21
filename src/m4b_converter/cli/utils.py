import re
import subprocess
from rich.console import Console
from datetime import datetime
from typing import Optional, Dict

console = Console()

def parse_metadata(metadata_str: Optional[str]) -> Dict[str, str]:
    """Convierte un string 'key1=value1,key2=value2' en un diccionario."""
    if not metadata_str:
        return {}
    return dict(pair.split("=") for pair in metadata_str.split(","))

def get_audio_duration(input_path: str) -> float:
    """Obtiene la duración del audio en segundos usando FFmpeg."""
    result = subprocess.run(
        ["ffmpeg", "-i", input_path],
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    # Busca líneas como "Duration: 00:03:45.23"
    match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}", result.stderr)
    if not match:
        raise ValueError("No se pudo obtener la duración del audio.")
    h, m, s = map(float, match.groups())
    return h * 3600 + m * 60 + s

def time_str_to_seconds(time_str: str) -> Optional[float]:
    """Convierte strings de tiempo (HH:MM:SS.ms o HH:MM:SS) a segundos.
    Retorna None si el formato es inválido (ej: 'N/A')."""
    if not time_str or time_str.strip().upper() == "N/A":
        console.log(f"[yellow]⚠️ Tiempo no válido ignorado: {time_str}[/yellow]")
        return None
    
    # Extrae HH, MM, SS.SSS con regex (admite varios formatos)
    time_match = re.match(
        r"^(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2}(?:\.\d+)?)$", 
        time_str.strip()
    )
    if not time_match:
        console.log(f"[yellow]⚠️ Formato de tiempo no reconocido: {time_str}[/yellow]")
        return None
    
    try:
        h = float(time_match.group("h"))
        m = float(time_match.group("m"))
        s = float(time_match.group("s"))
        return h * 3600 + m * 60 + s
    except ValueError:
        console.log(f"[red]❌ Error al convertir tiempo: {time_str}[/red]")
        return None

def total_duration(input_path: str) -> str:
    """Obtiene la duración del audio usando FFmpeg y lo retorna en formato string."""
    result = subprocess.run(
        ["ffmpeg", "-i", input_path],
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.\d{2}", result.stderr)
    if not match:
        raise ValueError("No se pudo obtener la duración del audio.")
    
    h = str(match.group(1))
    m = str(match.group(2))
    s = str(match.group(3))

    duration = f"{h + ":"+ m + ":" + s}"

    return duration