"""
Clean the app directories
"""
import shutil
from argparse import Namespace
from rich.console import Console
from rich.table import Table

from m4b_converter.settings import AppSettings
from m4b_converter.cli.utils import count_files_in_directory

def clean_directories(args: Namespace, console: Console) -> None:
    """
    Clean the app directories.
    """
    if not AppSettings.APP_DIR.exists():
        console.print(f"[bold red]Error:[/bold red] {AppSettings.APP_DIR} no existe.")
    
    temp_files = count_files_in_directory(AppSettings.TEMP_DIR)
    output_files = count_files_in_directory(AppSettings.OUTPUT_DIR)
    log_files = count_files_in_directory(AppSettings.LOGS_DIR)

    for directory in [AppSettings.TEMP_DIR, AppSettings.OUTPUT_DIR, AppSettings.LOGS_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    table = Table(title="[bold magenta]Directorios limpiados[/bold magenta]", border_style="blue", padding=(0, 2))
    table.add_column("Directory", style="cyan", justify="right")
    table.add_column("Files", style="green")

    table.add_row("Temp", f"{temp_files}")
    table.add_row("Output", f"{output_files}")
    table.add_row("Logs", f"{log_files}")

    console.print(table)