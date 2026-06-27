# Ejemplos Prácticos

## Escenario 1: Convertir un audiolibro MP3 a M4B

Tienes un audiolibro en MP3 con portada incrustada y quieres convertirlo a M4B con buena calidad y compresión.

```bash
# Analizar el archivo primero para conocer sus características
m4b analyze "Mi Audiolibro.mp3"

# Convertir con bitrate 64k (óptimo para voz) y mono
m4b convert "Mi Audiolibro.mp3" --bitrate 64k --channels 1

# La portada se extraerá automáticamente y se incluirá en el M4B
```

**Resultado:** `Mi Audiolibro.m4b` (~30-40% del tamaño original)

---

## Escenario 2: Procesar un directorio completo de audiolibros

Tienes un directorio con múltiples audiolibros en diferentes formatos y quieres convertirlos todos.

```bash
# Estructura de directorios
# audiolibros/
#   ├── Libro1.mp3
#   ├── Libro2.flac
#   └── Libro3.m4a

# Convertir todos los archivos con bitrate 96k y estéreo
m4b batch ./audiolibros/ --bitrate 96k --channels 2

# Si tienes subdirectorios, usar --recursive
m4b batch ./audiolibros/ --bitrate 64k --recursive
```

---

## Escenario 3: Extraer solo la portada de un archivo

Quieres extraer la portada de un audiolibro para usarla como miniatura.

```bash
# Extraer portada
m4b cover "Mi Audiolibro.mp3"

# La portada se guarda como "Mi Audiolibro_cover.jpg"
```

---

## Escenario 4: Flujo completo de trabajo con verificación

Un flujo completo con análisis, extracción de portada y conversión.

```bash
# 1. Analizar el archivo
m4b analyze "Libro.mp3"

# 2. Extraer la portada (opcional - se hará automáticamente en convert)
m4b cover "Libro.mp3"

# 3. Convertir a M4B
m4b convert "Libro.mp3" --bitrate 64k --channels 1

# 4. Verificar el resultado
ls -lh Libro.m4b
```

---

## Escenario 5: Optimización para diferentes tipos de contenido

### Audiolibro narrado (solo voz)
```bash
# Mono y bitrate bajo para máximo ahorro
m4b convert "voz.mp3" --bitrate 64k --channels 1
```

### Audiolibro con música de fondo
```bash
# Estéreo y bitrate medio para mejor calidad musical
m4b convert "voz_musica.mp3" --bitrate 128k --channels 2
```

### Producción de alta calidad (música + voz)
```bash
# Calidad superior para obras musicales
m4b convert "produccion.mp3" --bitrate 192k --channels 2
```

---

## Escenario 6: Mantenimiento - Limpieza de archivos

Limpieza regular de archivos temporales y convertidos para liberar espacio.

```bash
# Limpiar directorios temporales y de salida
m4b clean

# Verificar el espacio liberado
du -sh ~/.m4b_converter/
```

---

## Consejos de Uso

### 🎯 Recomendaciones de Bitrate según contenido

| Tipo de Contenido | Bitrate | Canales | Tamaño (por hora) |
|-------------------|---------|---------|-------------------|
| Voz sola | 64k | 1 | ~28 MB |
| Voz con música | 96k - 128k | 2 | ~43 - 57 MB |
| Música | 192k - 320k | 2 | ~86 - 144 MB |

### 💾 Ahorro de Espacio Estimado

- MP3 128k → M4B 64k: ~50% de reducción
- WAV → M4B 64k: ~90% de reducción
- FLAC → M4B 64k: ~80% de reducción