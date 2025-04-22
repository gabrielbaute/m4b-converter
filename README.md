# 📖 m4b-converter

**Herramienta CLI para convertir audios a formato M4B** con metadatos personalizados, capítulos y optimización de bitrate.  
Perfecto para audiolibros, podcasts o archivos de voz.

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Características

- ✅ Conversión a M4B desde MP3, WAV, M4A, etc.
- 📝 Metadatos personalizados (título, autor, género).
- ⏱️ Soporte para capítulos con marcas de tiempo.
- 🎚️ Optimización de bitrate (64kbps recomendado para voz).
- 📊 Barra de progreso con `rich`.
- 🔄 Uso de directorios temporales para seguridad.

## 📦 Instalación

1. **Requisitos**:  
   - Python 3.12+
   - [Poetry](https://python-poetry.org/) (recomendado) o `pip`

2. **Instalar con Poetry**:
   ```bash
   git clone https://github.com/gabrielbaute/m4b-converter.git
   cd m4b-converter
   poetry install
   ```

3. **Instalar con pip** (alternativa):
   ```bash
   pip install m4b-converter
   ```

## 🛠 Uso Básico

### Conversión simple:
```bash
m4b-converter "audio.mp3" --bitrate 64k --metadata "title=Mi Audiolibro,author=Autor"
```

### Mostrar versión:
```bash
m4b-converter --version
```
**Salida**:  
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📦 m4b-converter                      ┃
┡━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━┩
│  Versión         │ 0.2.1              │
│  Autor           │ Gabriel Baute      │
│  Licencia        │ MIT                │
└──────────────────────┴─────────────────┘
```

### Parámetros avanzados:
| Argumento          | Descripción                              | Ejemplo                  |
|--------------------|------------------------------------------|--------------------------|
| `-o OUTPUT_DIR`    | Directorio de salida (default: `output`) | `-o "mis_audiolibros"`   |
| `-b BITRATE`       | Bitrate (ej: 64k, 128k)                 | `-b 48k`                 |
| `-c CHANNELS`      | Canales (1=mono, 2=estéreo)             | `-c 1`                   |
| `-m METADATA`      | Metadatos en formato `key=value`        | `-m "title=El Principito"` |
| `--keep-temp`      | Conservar archivos temporales           | `--keep-temp`            |

## 🛠 Desarrollo

### Estructura del proyecto:
```
m4b-converter/
├── src/
│   └── m4b_converter/
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/          # Lógica de conversión
│       └── cli/           # Interfaz de comandos
├── tests/
├── pyproject.toml
└── .bumpver.toml          # Config de versionado
```


### Actualizar versión:
```bash
poetry run bumpver update --patch  # --minor o --major
```

## 📄 Licencia
MIT © [Gabriel Baute](https://github.com/gabrielbaute)  
