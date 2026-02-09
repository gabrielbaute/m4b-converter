import sys
from pathlib import Path
from rich.console import Console

from m4b_converter.cli.parser import create_parser
from m4b_converter.cli.commands import analyze_audiobook, handle_convert, handle_cover, show_version, handle_batch, clean_directories

def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    console = Console()

    if args.command == "version":
        show_version(console)
    elif args.command == "analyze":
        analyze_audiobook(Path(args.file), console)
    elif args.command == "convert":
        handle_convert(args, console)
    elif args.command == "cover":
        handle_cover(Path(args.file), console)
    elif args.command == "batch":
        handle_batch(args, console)
    elif args.command == "clean":
        clean_directories(args, console)

if __name__ == "__main__":
    main()