from pathlib import Path
from rich.table import Table
from argparse import Namespace
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from m4b_converter.enums import Bitrate
from m4b_converter.managers import WorkflowManager
from m4b_converter.schemas import ConversionResult
from m4b_converter.cli.utils import convert_bytes_to_mb, parse_seconds

def handle_convert(args: Namespace, console: Console):
    manager = WorkflowManager()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task_id = progress.add_task(f"[cyan]Procesando {args.input.name}...", total=100)
        
        def update_progress(percent: float):
            progress.update(task_id, completed=percent)

        result: ConversionResult = manager.process_file(
            input_path=args.input,
            bitrate=Bitrate(args.bitrate),
            channels=args.channels,
            output_dir=Path(args.output_dir) if args.output_dir else None,
            progress_callback=update_progress
        )

    if result:
        # Convertimos bytes a MB
        size_original_mb = convert_bytes_to_mb(result.size_original_bytes)
        size_final_mb = convert_bytes_to_mb(result.size_final_bytes)
        
        # Formatear unidades de tiempo
        total_convert_time = (result.timestamp_end - result.timestamp_start).total_seconds()
        file_duration = parse_seconds(result.duration_seconds)
        conversion_duration = parse_seconds(total_convert_time)

        # Diagramamos la tabla
        table = Table(title=f"[bold magenta]¡Éxito!Resultado de la conversión[/bold magenta]: {result.task_id}", border_style="blue")
        table.add_column("Atributo", style="cyan", justify="right")
        table.add_column("Valor", style="green")

        # Vaciado de datos
        table.add_row("ID de tarea", f"{result.task_id}")
        table.add_row("Tiempo de inicio", f"{result.timestamp_start}")
        table.add_row("Tiempo de finalización", f"{result.timestamp_end}")
        table.add_row("Tiempo de conversión", conversion_duration)
        table.add_row("Duracón del archivo", file_duration)
        table.add_row("Tamaño original", f"{size_original_mb:.2f} MB")
        table.add_row("Tamaño final", f"{size_final_mb:.2f} MB")
        table.add_row("Formato final", f"{result.output_path.suffix[1:]}")
        table.add_row("Bitrate final", f"{result.bitrate_final}")
        table.add_row("Codec final", f"{result.codec_final}")
        table.add_row("Ratio de compresión", f"{result.compression_ratio*100:.1f}%")
        table.add_row("Espacio ahorrado", f"{result.space_saved_mb} MB")

        console.print(table)

    else:
        console.print("[bold red]Error durante la conversión.[/bold red]")