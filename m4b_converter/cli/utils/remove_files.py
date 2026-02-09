from pathlib import Path

def remove_file(path: Path, ext: str) -> bool:
    """
    Remove the file with the given extension

    Args:
        path (Path): Path to the file
        ext (str): Extension of the file

    Returns:
        bool: True if the file was removed, False otherwise
    """
    file = path / f"*.{ext}"
    if file.exists():
        file.unlink()
        return True
            
    return False