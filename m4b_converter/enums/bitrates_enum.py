from enum import StrEnum

class Bitrate(StrEnum):
    """
    Enum para los bitrates de audio optimizados para audiolibros en formato M4B.

    Attributes:
        B_64K (str): 64 kbps - Bitrate ideal para audiolibros narrados con voz clara, excelente relación calidad/tamaño para largas duraciones.
        B_96K (str): 96 kbps - Calidad mejorada para audiolibros con efectos de sonido o música incidental, manteniendo un tamaño moderado.
        B_128K (str): 128 kbps - Estándar recomendado para audiolibros con música de fondo o contenido musical, buena fidelidad en M4B.
        B_192K (str): 192 kbps - Calidad superior para audiolibros con banda sonora compleja o grabaciones de estudio.
        B_256K (str): 256 kbps - Alta fidelidad para audiolibros premium, ideal cuando el contenido incluye material musical extenso.
        B_320K (str): 320 kbps - Calidad máxima para audiolibros de referencia, usado en producciones donde la calidad de audio es crítica.
    """
    B_64K = "64k"
    B_96K = "96k"
    B_128K = "128k"
    B_192K = "192k"
    B_256K = "256k"
    B_320K = "320k"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value