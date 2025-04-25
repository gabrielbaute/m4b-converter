import sys
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.markdown import Markdown

from m4b_converter.cli.parser import generate_parser
from m4b_converter.cli.utils import parse_metadata, get_audio_duration, time_str_to_seconds, total_duration
from m4b_converter.cli.version import show_version, __version__
from m4b_converter.core import M4bConverter, Mp3Merger

console = Console()


def main():
    parser = generate_parser()
    args = parser.parse_args()

    # Manejar --version primero
    if args.version:
        show_version()
        sys.exit(0)

    # Si no se especifica comando, mostrar ayuda
    if not hasattr(args, "command"):
        console.print(Markdown("## 🚀 Uso básico:"))
        parser.print_help()
        return

    # Procesar metadatos (si existen)
    metadata = parse_metadata(args.metadata) if args.metadata else None

    # Obtiene la duración en segundos del archivo
    duration = get_audio_duration(args.input)
    total_file_duration = total_duration(args.input)

    # Inicializar conversor común
    converter = M4bConverter(
        input_path=args.input,
        output_dir=args.output_dir,
        temp_dir=args.temp_dir,
        metadata=metadata
    )

    if args.command == "merge":
        merger = Mp3Merger(args.input_dir, args.output_dir)
        metadata = {}
        if args.title:
            metadata["title"] = args.title
        if args.author:
            metadata["artist"] = args.author
        
        merger.merge(metadata=metadata)

    # Barra de progreso común
    def progress_callback(time_str: str):
        """Actualiza la barra de progreso con el tiempo procesado."""
        current_sec = time_str_to_seconds(time_str)
        desc = f"⏳ [bold green]{time_str}[/bold green]" if args.command == "convert" else f"⚡ [bold yellow]{time_str}[/bold yellow]"
        progress.update(task, completed=current_sec, description=desc)

    # Configurar barra según el comando
    progress_title = {
        "convert": "[cyan bold blink]Convirtiendo...[/cyan bold blink]",
        "optimize": "[yellow bold blink]Optimizando...[/yellow bold blink]"
    }

    with Progress(
        TextColumn(progress_title[args.command]),
        TextColumn("|"),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("|"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        TextColumn("•"),
        TextColumn(f"[bold green]Duración total[/bold green]: [bold bright_blue]{total_file_duration}[/bold bright_blue]"),
        console=console
    ) as progress:
        duration = get_audio_duration(args.input)
        task = progress.add_task("[cyan bold]Iniciando...[/cyan bold]", total=duration)

        try:
            if args.command == "convert":
                converter.convert_to_m4b(
                    bitrate=args.bitrate,
                    channels=args.channels,
                    threads=args.threads,
                    progress_callback=progress_callback,
                    remove_temp=not args.keep_temp
                )
            elif args.command == "optimize":
                converter.optimize_m4b(
                    bitrate=args.bitrate,
                    channels=args.channels,
                    threads=args.threads,
                    progress_callback=progress_callback,
                    remove_temp=not args.keep_temp
                )

            progress.console.print(f"[green]✅ Listo! Archivo guardado en: [bold]{converter.output_path}")

        except Exception as e:
            progress.console.print(f"[red]❌ Error: {e}")
            raise