from pathlib import Path
from m4b_converter.settings import M4bLogger
from m4b_converter.services import ExtractCoverService, AudioAnalyzerService

M4bLogger.setup_logging()

file: Path = Path("C:/Users/gabri/Downloads/Una Corte de Hielo y Estrellas.mp3")

analyzer = AudioAnalyzerService(file_path=file)
raw_data_test = analyzer.get_raw_info()

cover_extractor = ExtractCoverService(file_path=file)
info = cover_extractor.extract_cover(raw_data=raw_data_test)