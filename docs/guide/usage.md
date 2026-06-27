# Uso Básico

## Comandos

### Convertir

```bash
m4b convert archivo.mp3 --bitrate 64k --channels 1
```

Opciones:
- `-b, --bitrate`: 64k, 96k, 128k, etc.
- `-c, --channels`: 1 (mono) o 2 (estéreo)
- `-o, --output-dir`: Directorio de salida

### Analizar

```bash
m4b analyze archivo.mp3
```

### Procesar por lote

```bash
m4b batch ./directorio/ --bitrate 64k
```

### Extraer portada

```bash
m4b cover archivo.mp3
```

### Limpiar temporales

```bash
m4b clean
```

### Versión

```bash
m4b version
```