from typing import Union

def parse_seconds(seconds: Union[float, int]) -> str:
    """
    Convierte segundos a formato hh:mm:ss.

    Args:
        seconds (Union[float, int]): Segundos a convertir.

    Returns:
        str: Formato hh:mm:ss.
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    