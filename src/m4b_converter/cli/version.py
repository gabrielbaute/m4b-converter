from rich.console import Console
from rich.table import Table

__version__ = "0.2.2"

def show_version():
    """Muestra la versión en una tabla estilo Rich."""
    console = Console()
    table = Table(
        title="[bold magenta]m4b-converter[/bold magenta]",
        show_header=False,
        border_style="blue",
        padding=(0, 2),
    )
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")
    
    table.add_row("[yellow]Build[/yellow]", "[bold]stable[/bold]")
    table.add_row("Versión", f"[bold]{__version__}[/bold]")
    table.add_row("Autor", "Gabriel Baute")
    table.add_row("Licencia", "MIT")
    table.add_row("Repo", "https://github.com/gabrielbaute/m4b-converter")

    console.print(table)