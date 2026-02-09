from pathlib import Path
from m4b_converter.settings import M4bLogger
from m4b_converter.services import AudioAnalyzerService

M4bLogger.setup_logging()

file: Path = Path("C:/Users/gabri/Downloads/Una Corte de Hielo y Estrellas.mp3")

analyzer = AudioAnalyzerService(file_path=file)
info = analyzer.analyze()

print(info.dict())