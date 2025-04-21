from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TextColumn, TimeElapsedColumn
from rich.markdown import Markdown

from cli.parser import generate_parser
from cli.utils import parse_metadata, get_audio_duration, time_str_to_seconds, total_duration
from m4b_converter import M4bConverter

console = Console()


def main():

    parser = generate_parser()
    args = parser.parse_args()
    
    # Mostrar ayuda con estilo
    if not args.input:
        console.print(Markdown("## 🚀 Uso básico:"))
        parser.print_help()
        return
    
    # Procesar metadatos
    metadata = parse_metadata(args.metadata)
    # Obtiene la duración en segundos del archivo
    duration = get_audio_duration(args.input)
    total_file_duration = total_duration(args.input)
    
    # Inicializar conversor
    converter = M4bConverter(
        input_path=args.input,
        output_dir=args.output_dir,
        temp_dir=args.temp_dir,
        metadata=metadata
    )
    
    # Barra de progreso con Rich
    def progress_callback(time_str: str):
        """Actualiza la barra de progreso con el tiempo procesado."""
        progress.update(task, advance=1, description=f"⏳ [bold green]{time_str}[/bold]")
    
    # Convertir con Rich
    with Progress(
        TextColumn("[cyan bold blink]Convirtiendo... [/cyan bold blink]"),
        TextColumn("|"),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("|"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
        TextColumn("•"),
        TextColumn(f"[bold green]Duración total del archivo[/bold green]: [bold bright_blue]{total_file_duration}[/bold bright_blue]"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan bold]Iniciando... [/cyan bold]", total=duration)
        
        def progress_callback(time_str: str):
            """Actualiza la barra con el tiempo real procesado."""
            current_sec = time_str_to_seconds(time_str)
            if current_sec is not None:
                progress.update(task, completed=current_sec, description=f"[bold bright_blue]Tiempo convertido:[/bold bright_blue] [bold green]{time_str}[/bold green]")
        
        try:
            converter.convert_to_m4b(
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

if __name__ == "__main__":
    main()