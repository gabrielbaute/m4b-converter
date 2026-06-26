from enum import IntEnum

class AudioChannels(IntEnum):
    """
    Canales de audio disponibles para audiolibros en formato M4B.

    Attributes:
        MONO (int): Monocanal - Ideal para audiolibros narrados con voz sola, reduce el tamaño del archivo y es suficiente para contenido hablado.
        STEREO (int): Estéreo - Dos canales, recomendado para audiolibros con música de fondo, efectos sonoros o producciones inmersivas.
    """
    MONO = 1
    STEREO = 2
    
    def __str__(self):
        return self.value