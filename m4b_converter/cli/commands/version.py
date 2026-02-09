"""
Version command for the CLI.
"""
from rich.console import Console
from rich.table import Table

from m4b_converter.settings import AppSettings

def show_version(console: Console) -> None:
    """
    Muestra la versión de la CLI.

    Args:
        console (Console): Objeto Console.

    Returns:
        None
    """
    console = Console()
    table = Table(
        title="[bold magenta]M4B Converter[/bold magenta]",
        show_header=False,
        border_style="blue",
        padding=(0, 2),
    )
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")
    
    table.add_row("[yellow]Build[/yellow]", "[bold]stable[/bold]")
    table.add_row("Versión", f"[bold]{AppSettings.VERSION}[/bold]")
    table.add_row("Author", "Gabriel Baute")
    table.add_row("License", "MIT")
    table.add_row("Repo", "https://github.com/gabrielbaute/m4b-converter")

    console.print(table)