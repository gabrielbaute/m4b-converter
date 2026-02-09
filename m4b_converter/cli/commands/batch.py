from pathlib import Path
from rich.table import Table
from argparse import Namespace
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from m4b_converter.enums import Bitrate
from m4b_converter.managers import WorkflowManager
from m4b_converter.cli.utils import convert_bytes_to_mb

def handle_batch(args: Namespace, console: Console):
    manager = WorkflowManager()
    input_dir = Path(args.input_dir)
    
    if not input_dir.is_dir():
        console.print(f"[bold red]Error:[/bold red] {input_dir} no es un directorio válido.")
        return

    # Usamos Progress de Rich para el lote completo
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        # Encontramos archivos (puedes usar tu util count_files o glob aquí)
        files = list(input_dir.glob("*.mp3")) # Simplificado, podrías usar varias extensiones
        overall_task = progress.add_task(f"[yellow]Procesando lote...", total=len(files))
        
        results = []
        
        for file_path in files:
            progress.update(overall_task, description=f"[cyan]Convirtiendo: {file_path.name}")
            
            # El callback aquí podría actualizar una sub-barra si quisieras
            res = manager.process_file(
                input_path=file_path,
                bitrate=Bitrate(args.bitrate),
                channels=args.channels,
                output_dir=Path(args.output_dir) if args.output_dir else None
            )
            if res:
                results.append(res)
            progress.advance(overall_task)

    # Mostrar tabla resumen
    if results:
        summary_table = Table(title="[bold green]Resumen de Procesamiento por Lote[/bold green]")
        summary_table.add_column("Archivo", style="cyan")
        summary_table.add_column("Original", justify="right")
        summary_table.add_column("Final", justify="right")
        summary_table.add_column("Ahorro %", style="green", justify="right")

        total_saved = 0
        for r in results:
            orig_mb = convert_bytes_to_mb(r.size_original_bytes)
            final_mb = convert_bytes_to_mb(r.size_final_bytes)
            summary_table.add_row(
                r.output_path.name,
                f"{orig_mb:.2f} MB",
                f"{final_mb:.2f} MB",
                f"{r.compression_ratio*100:.1f}%"
            )
            total_saved += r.space_saved_mb

        console.print(summary_table)
        console.print(f"\n[bold gold1]Ahorro total de espacio: {total_saved:.2f} MB[/bold gold1]")
    else:
        console.print("[yellow]No se procesó ningún archivo con éxito.[/yellow]")