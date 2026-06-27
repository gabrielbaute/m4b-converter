# Comandos CLI

Esta guía detalla todos los comandos disponibles en la interfaz de línea de comandos (CLI) de M4B Converter.

## `m4b convert`

Convierte un archivo de audio a formato M4B.

```bash
m4b convert <input> [opciones]
```

**Argumentos:**
- `<input>`: Ruta al archivo de audio a convertir (obligatorio)

**Opciones:**
| Opción | Descripción | Valores | Default |
|--------|-------------|---------|---------|
| `-b, --bitrate` | Bitrate de salida | 64k, 96k, 128k, 192k, 256k, 320k | 64k |
| `-c, --channels` | Canales de audio | 1 (mono), 2 (estéreo) | 2 |
| `-o, --output-dir` | Directorio de salida | Ruta válida | Directorio actual |

**Ejemplos:**
```bash
# Conversión básica
m4b convert audio.mp3

# Conversión con bitrate y canales específicos
m4b convert audio.mp3 --bitrate 64k --channels 1

# Especificar directorio de salida
m4b convert audio.mp3 --output-dir ./audiolibros/
```

---

## `m4b analyze`

Analiza un archivo de audio y muestra información detallada.

```bash
m4b analyze <file>
```

**Argumentos:**
- `<file>`: Ruta al archivo de audio a analizar (obligatorio)

**Información mostrada:**
- Tamaño del archivo
- Duración total
- Formato y códec
- Bitrate
- Frecuencia de muestreo
- Canales
- Metadatos (título, artista, álbum, etc.)

**Ejemplo:**
```bash
m4b analyze mi_audiolibro.mp3
```

---

## `m4b batch`

Procesa todos los archivos de audio compatibles en un directorio.

```bash
m4b batch <input_dir> [opciones]
```

**Argumentos:**
- `<input_dir>`: Directorio con los archivos de audio (obligatorio)

**Opciones:**
| Opción | Descripción | Valores | Default |
|--------|-------------|---------|---------|
| `-b, --bitrate` | Bitrate de salida | 64k, 96k, 128k, etc. | 64k |
| `-c, --channels` | Canales de audio | 1, 2 | 1 |
| `-o, --output-dir` | Directorio de salida | Ruta válida | Directorio de la app |
| `--recursive` | Buscar en subdirectorios | - | No |

**Extensiones compatibles:** `.mp3`, `.m4a`, `.wav`, `.flac`, `.opus`, `.ogg`

**Ejemplo:**
```bash
m4b batch ./audiolibros/ --bitrate 64k --recursive
```

---

## `m4b cover`

Extrae la portada incrustada en un archivo de audio.

```bash
m4b cover <file>
```

**Argumentos:**
- `<file>`: Ruta al archivo de audio (obligatorio)

**Salida:** La portada se guarda como `{nombre}_cover.jpg` en el mismo directorio.

**Ejemplo:**
```bash
m4b cover audiolibro.mp3
```

---

## `m4b clean`

Limpia los directorios temporales y de salida de la aplicación.

```bash
m4b clean
```

**Elimina:**
- Archivos temporales de conversión
- Archivos de salida anteriores
- Logs antiguos

---

## `m4b version`

Muestra información de versión de la aplicación.

```bash
m4b version
```

**Información mostrada:**
- Versión actual
- Autor
- Licencia
- Repositorio