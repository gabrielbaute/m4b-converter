# 📖 m4b-converter

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Herramienta CLI para convertir y optimizar audios a M4B**  
✨ Conversiones con metadatos ✨ Optimización de bitrate ✨ Capítulos con marcas de tiempo

Este prouecto surgió como consecuencia de que, cuando suelo buscar audiolibros, tiendo a encontrarlos en mp3, y la mayoría de los conversores que he encontrado (incluso el que viene incluído dentro de #AudiobookShelf) suelen deformarme mucho el audio o tiendo a perder calidad en él. El formato m4b es el estándar definido para audiolibros (aunque pueda usarse .m4a, que en esencia es casi idéntico, la convención es tratar las pistas de música en m4a y de audiolibros en m4b). Ciertamente, un formato m4b es mucho más eficiente y cuidadoso con mi poco espacio en disco que el mp3, y por eso decidí emprender este proyecto.

Además de los comandos mencionados, se incluyeron opciones como seleccionar cuántos núcleos del procesador se deben emplear durante una conversión (por defecto es 1). **Ffmepeg es requerido**, así que debes tenerlo previamente instalado en tu equipo.

Este proyecto está inspirado, naturalmente, en audiobookshelf, una aplicación de la que soy fan y  que uso de manera asidua.

## 🚀 Características
- ✅ **Conversión** a M4B desde MP3, WAV, FLAC, etc.
- 🔄 **Optimización** de archivos M4B existentes (bitrate/canales).
- 📝 **Metadatos personalizados** (título, autor, género).
- ⏱️ **Capítulos** desde archivos de texto (próximamente).
- 📊 **Barra de progreso** interactiva con `rich`.

### Características futuras
Algunas de las características que planeo incluir más adelante:
- Convertir de m4b a mp3 en caso de que el usuario lo desee.
- Incorporar metadata de marcas de tiempo de los capítulos
- Generar un .json con la metadata del audiolibro en formato de #Audiobookshelf
- ✅ Unificar varios archivos mp3 en uno solo y convertir dicho archivo a m4b (si el usuario lo requiere) (**Completada**)

## 💾 Instalación
```bash
git clone https://github.com/gabrielbaute/m4b-converter.git
cd m4b-converter
poetry install  # o pip install .
```

## 🛠 Uso

### 1. Convertir un archivo a M4B
```bash
m4b-converter convert
    --bitrate 128k \
    --channels 2 \
    --output-dir .\
    "audio.mp3"
```

### 2. Optimizar un M4B existente
```bash
m4b-converter optimize "libro.m4b" \
    --bitrate 64k \
    --channels 1 \
```

### 3. Fusionar varios archivos mp3 en uno solo
```bash
m4b-converter merge "carpeta_audios/" \
    --title "El Principito" \
    --author "Saint-Exupéry" \
    --output-dir "resultados/"
```

### 📌 Opciones comunes
| Argumento          | Descripción                              | Valores típicos       |
|--------------------|------------------------------------------|-----------------------|
| `-b, --bitrate`    | Calidad de audio (bitrate)               | `64k`, `128k`         |
| `-c, --channels`   | Canales (`1`=mono, `2`=estéreo)          | `1` (voz), `2` (música)|
| `-o, --output-dir` | Directorio de salida                     | `./output`            |


## 📄 Licencia
MIT © [Gabriel Baute](https://github.com/gabrielbaute/m4b-converter/LICENSE)
