import argparse
from m4b_converter.cli.version import __version__

def generate_parser():
    # Parser principal
    parser = argparse.ArgumentParser(
        description="📖 Conversor y optimizador de audios a M4B.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-v", "--version", action="store_true", help="Mostrar versión y salir")
    
    # Subcomandos: convert y optimize
    subparsers = parser.add_subparsers(dest="command", required=False, help="Comandos disponibles")

    # -------------------------------------------
    # Subcomando: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convertir un archivo de audio a M4B"
    )
    convert_parser.add_argument("input", type=str, help="Ruta del archivo de entrada (MP3, WAV, etc.)")
    convert_parser.add_argument("-o", "--output-dir", type=str, default="output", help="Directorio de salida")
    convert_parser.add_argument("-t", "--temp-dir", type=str, default="temp", help="Directorio para archivos temporales")
    convert_parser.add_argument("-b", "--bitrate", type=str, default="64k", help="Bitrate (ej: 64k, 128k)")
    convert_parser.add_argument("-c", "--channels", type=int, default=1, help="Número de canales (1=mono, 2=estéreo)")
    convert_parser.add_argument("-m", "--metadata", type=str, help="Metadatos en formato 'title=Mi Libro,author=Autor'")
    convert_parser.add_argument("--keep-temp", action="store_true", help="No borrar archivos temporales")
    convert_parser.add_argument("--threads", type=int, default=1, help="Hilos para FFmpeg")

    # -------------------------------------------
    # Subcomando: optimize
    # -------------------------------------------
    optimize_parser = subparsers.add_parser(
        "optimize",
        help="Optimizar un archivo M4B existente (reducir bitrate, canales, etc.)"
    )
    optimize_parser.add_argument("input", type=str, help="Ruta del archivo M4B a optimizar")
    optimize_parser.add_argument("-o", "--output-dir", type=str, default="output", help="Directorio de salida")
    optimize_parser.add_argument("-t", "--temp-dir", type=str, default="temp", help="Directorio para archivos temporales")
    optimize_parser.add_argument("-b", "--bitrate", type=str, default="64k", help="Bitrate objetivo (ej: 32k, 64k)")
    optimize_parser.add_argument("-c", "--channels", type=int, default=1, help="Canales de salida (1=mono, 2=estéreo)")
    optimize_parser.add_argument("-m", "--metadata", type=str, help="Metadatos actualizados 'title=Nuevo Título'")
    optimize_parser.add_argument("--keep-temp", action="store_true", help="No borrar archivos temporales")
    optimize_parser.add_argument("--threads", type=int, default=1, help="Hilos para FFmpeg")

    # -------------------------------------------
    # Subcomando: merge
    # -------------------------------------------
    merge_parser = subparsers.add_parser(
        "merge", 
        help="Fusionar archivos MP3"
    )
    merge_parser.add_argument("input_dir", help="Directorio con MP3s")
    merge_parser.add_argument("-o", "--output-dir", default="output")
    merge_parser.add_argument("--title", help="Título del audiolibro")
    merge_parser.add_argument("--author", help="Autor del audiolibro")

    return parser