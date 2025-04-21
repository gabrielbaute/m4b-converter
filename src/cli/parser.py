import argparse

def generate_parser():
    parser = argparse.ArgumentParser(
        description="📖 Conversor de audio a M4B con metadatos y capítulos.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Argumentos principales
    parser.add_argument("input", type=str, help="Ruta del archivo de entrada (MP3, WAV, etc.)")
    parser.add_argument("-o", "--output-dir", type=str, default="output", help="Directorio de salida")
    parser.add_argument("-t", "--temp-dir", type=str, default="temp", help="Directorio para archivos temporales")
    
    # Opciones de audio
    parser.add_argument("-b", "--bitrate", type=str, default="64k", help="Bitrate (ej: 64k, 128k)")
    parser.add_argument("-c", "--channels", type=int, default=1, help="Número de canales (1=mono, 2=estéreo)")
    
    # Metadatos
    parser.add_argument("-m", "--metadata", type=str, help="Metadatos en formato 'title=Mi Libro,author=Autor'")
    
    # Opciones avanzadas
    parser.add_argument("--keep-temp", action="store_true", help="No borrar archivos temporales")
    parser.add_argument("--threads", type=int, default=1, help="Hilos para FFmpeg")

    return parser