from pathlib import Path

def count_files_in_directory(directory: Path) -> int:
    """
    Count the number of files in a directory.

    Args:
        directory (Path): Path to the directory.

    Returns:
        int: Number of files in the directory.
    """
    return len(list(directory.glob("*")))