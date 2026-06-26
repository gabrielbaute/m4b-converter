from pathlib import Path
from argparse import ArgumentParser

from m4b_converter.enums import Bitrate

def create_parser() -> ArgumentParser:
    """
    Parser de comandos de entrada para la CLI.

    Returns:
        ArgumentParser: Objeto ArgumentParser.
    """
    parser = ArgumentParser(
        prog="M4B Converter",
        usage="Convierte tus archivos de audiolibro",
        description="Convierte archivos de audiolibro a m4b más optimizados",
        add_help=True,
        allow_abbrev=True,
        exit_on_error=True
        )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # -------------------------------------------
    # Subcommand: version
    # -------------------------------------------
    subparsers.add_parser("version", help="Muestra la versión de la CLI.")

    # -------------------------------------------
    # Subcommand: analyze
    # -------------------------------------------
    analyze_parser = subparsers.add_parser("analyze", help="Analiza el archivo de un audiolibro.")
    analyze_parser.add_argument("file", type=str, help="Ruta hacia el archivo de audio a analizar.")
    
    # -------------------------------------------
    # Subcommand: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser("convert", help="Convierte un archivo de audio a m4b")
    convert_parser.add_argument("input", type=Path, help="Ruta al archivo de audio")
    convert_parser.add_argument("-b", "--bitrate", type=str, default="64k", choices=[b.value for b in Bitrate])
    convert_parser.add_argument("-c", "--channels", type=int, default=2, choices=[1, 2], help="Cantidad de canales, 1 0 2, 2 por default.")
    convert_parser.add_argument("-o","--output-dir", type=str, default=None, help="Directorio de salida para la conversión")

    # -------------------------------------------
    # Subcommand: cover
    # -------------------------------------------
    cover_parser = subparsers.add_parser("cover", help="Extrae el cover/portada del archivo de audio de un audiolibro.")
    cover_parser.add_argument("file", type=str, help="Ruta al archivo de audio al que extraer el cover.")

    # -------------------------------------------
    # Subcommand: batch
    # -------------------------------------------
    batch_parser = subparsers.add_parser("batch", help="Convierte a m4b todos los archivos de audio que hay en un directorio.")
    batch_parser.add_argument("input_dir", type=str, help="Directorio con archivos de audio")
    batch_parser.add_argument("-b", "--bitrate", type=str, default="64k", choices=[b.value for b in Bitrate])
    batch_parser.add_argument("-c", "--channels", type=int, default=1, choices=[1, 2])
    batch_parser.add_argument("-o", "--output-dir", type=str, default=None, help="Directorio de salida para la conversión")

    # -------------------------------------------
    # Subcommand: clean
    # -------------------------------------------
    subparsers.add_parser("clean", help="Clean the app directories")
    
    return parser