from pathlib import Path
from argparse import ArgumentParser

from m4b_converter.enums import Bitrate

def create_parser() -> ArgumentParser:
    """
    Parser de comandos de entrada.

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
    
    subparsers = parser.add_subparsers(dest="command", help="Commands available")
    
    # -------------------------------------------
    # Subcommand: version
    # -------------------------------------------
    subparsers.add_parser("version", help="Shows CLI version")

    # -------------------------------------------
    # Subcommand: analyze
    # -------------------------------------------
    analyze_parser = subparsers.add_parser("analyze", help="Analyze an audiobook file")
    analyze_parser.add_argument("file", type=str, help="Path to the video file to analyze")
    
    # -------------------------------------------
    # Subcommand: convert
    # -------------------------------------------
    convert_parser = subparsers.add_parser("convert", help="Convert an audiobook file")
    convert_parser.add_argument("input", type=Path, help="Ruta al archivo de audio")
    convert_parser.add_argument("--bitrate", type=str, default="64k", choices=[b.value for b in Bitrate])
    convert_parser.add_argument("--channels", type=int, default=1, choices=[1, 2])
    convert_parser.add_argument("--output-dir", type=str, default=None, help="Directorio de salida para la conversión")

    # -------------------------------------------
    # Subcommand: cover
    # -------------------------------------------
    cover_parser = subparsers.add_parser("cover", help="Extract cover from an audiobook file")
    cover_parser.add_argument("file", type=str, help="Path to the video file to analyze")

    # -------------------------------------------
    # Subcommand: batch
    # -------------------------------------------
    batch_parser = subparsers.add_parser("batch", help="Convert a directory of audiobooks")
    batch_parser.add_argument("input_dir", type=str, help="Directorio con archivos de audio")
    batch_parser.add_argument("--bitrate", type=str, default="64k", choices=[b.value for b in Bitrate])
    batch_parser.add_argument("--channels", type=int, default=1, choices=[1, 2])
    batch_parser.add_argument("--output-dir", type=str, default=None, help="Directorio de salida para la conversión")

    # -------------------------------------------
    # Subcommand: clean
    # -------------------------------------------
    subparsers.add_parser("clean", help="Clean the app directories")
    
    return parser