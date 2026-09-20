# Topología de monitoreo PNETLab

Generador offline de diagramas de una red de laboratorio con sedes en Bogotá,
Cali y Medellín. Una única fuente Python produce archivos draw.io, SVG y GraphML.
No se conecta a los equipos ni modifica su configuración.

![Topología lógica del laboratorio](ejemplos/laboratorio.svg)

## Inicio rápido

Requiere Python 3.8 o superior. No necesita paquetes externos ni Internet.
Desde la carpeta del proyecto:

```bash
python3 generar_topologia.py
```

En Windows también puedes usar `py generar_topologia.py`.
El comando crea la carpeta `diagramas/` con tres archivos:

| Archivo | Uso |
| --- | --- |
| `laboratorio.drawio` | Equipos, etiquetas y conexiones editables en draw.io. |
| `laboratorio.svg` | Visualización en navegador o edición vectorial. |
| `laboratorio.graphml` | Intercambio de nodos y conexiones entre editores compatibles. |

GraphML conserva etiquetas y atributos de posición, pero cada editor puede
interpretar el diseño de forma diferente. Ningún formato garantiza la misma
apariencia en todos los programas.

## Comandos

```bash
# Consultar opciones
python3 generar_topologia.py --help

# Generar en otra carpeta
python3 generar_topologia.py --salida mi_topologia

# Regenerar archivos existentes (reemplaza cualquier edición manual)
python3 generar_topologia.py --sobrescribir

# Actualizar los ejemplos incluidos en el repositorio
python3 generar_topologia.py --salida ejemplos --sobrescribir
```

## Contenido

| Ruta | Descripción |
| --- | --- |
| `generar_topologia.py` | Datos del laboratorio y exportadores, sin dependencias. |
| `ejemplos/` | Diagramas ya generados y versionados. |
| `docs/TOPOLOGIA.md` | Alcance, datos confirmados y limitaciones. |
| `docs/GITHUB.md` | Pasos para subir el proyecto a GitHub. |
| `diagramas/` | Salida local; excluida de Git. |

## Personalizar la red

Edita las llamadas a `nodo(...)` y `enlace(...)` que llenan `NODOS` y `ENLACES`:

```python
nodo('equipo_nuevo', 'Nombre del equipo\nIP: por definir', 100, 1800)
enlace('swbog', 'equipo_nuevo', 'Conexión de laboratorio')
```

Cada identificador de nodo debe ser único; los enlaces deben utilizar
identificadores existentes. Las coordenadas y dimensiones determinan la
disposición en draw.io y SVG. Si añades equipos fuera del lienzo actual,
amplía también las dimensiones del lienzo en los exportadores.

## Abrir los resultados

- draw.io: abre `ejemplos/laboratorio.drawio` como archivo de diagrama.
- Navegador: abre `ejemplos/laboratorio.svg`.
- Editor compatible con GraphML: importa `ejemplos/laboratorio.graphml`.

## Estado del proyecto

Los diagramas documentan el último estado compartido del laboratorio; no son
una comprobación de conectividad ni de disponibilidad. Consulta
[los detalles de la topología](docs/TOPOLOGIA.md).

No se ha seleccionado una licencia de distribución para este proyecto.
