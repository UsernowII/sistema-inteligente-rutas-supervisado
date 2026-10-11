# Descripción de los datos

## Fuente y procedencia

No se recibieron ni se identificaron en los archivos del proyecto registros reales de viajes, pasajeros, horarios o tiempos del sistema de transporte. De acuerdo con la consigna, se construyó un dataset de muestra sintético.

La fuente estructural son los hechos de estaciones y conexiones definidos en `knowledge_base.py`, retomados del proyecto académico de la actividad 2. `generate_dataset.py` produce una fila para cada par ordenado de estaciones distintas y calcula el número mínimo de tramos con una búsqueda en anchura sobre esa red. No se consultó ni se presenta una fuente externa de datos operativos.

El archivo `data/trips_simplified.csv` contiene 72 filas: nueve estaciones de origen por ocho destinos diferentes de cada origen. Por ser sintético y derivado de una red pequeña, sirve para mostrar el flujo de aprendizaje supervisado, pero no representa la demanda ni la operación real de TransMilenio.

## Campos del CSV

| Campo | Tipo | Uso |
|---|---|---|
| `origin` | Texto | Nombre legible de la estación de origen. |
| `destination` | Texto | Nombre legible de la estación de destino. |
| `origin_index` | Entero | Posición de origen en la lista fija de estaciones; característica del modelo. |
| `destination_index` | Entero | Posición de destino en la lista fija de estaciones; característica del modelo. |
| `order_gap` | Entero | Diferencia absoluta entre los índices de origen y destino; característica del modelo. |
| `segments` | Entero | Número de tramos de la ruta mínima; se usa para derivar y verificar la etiqueta, no como característica de entrada. |
| `route_class` | Texto | Etiqueta objetivo que el modelo aprende a predecir: `corta`, `media` o `larga`. |

## Definición de la etiqueta

- `corta`: de 1 a 2 tramos.
- `media`: de 3 a 4 tramos.
- `larga`: 5 tramos o más.

La distribución creada es: 32 viajes cortos, 26 medios y 14 largos. La división estratificada fija (semilla 42) usa 53 ejemplos para entrenamiento y 19 para prueba.

## Consideraciones

Los índices son una codificación didáctica de las nueve estaciones, no coordenadas geográficas. `order_gap` deriva de esos índices. La etiqueta se calcula desde la misma red simplificada con búsqueda BFS; por tanto, el dataset no es evidencia independiente sobre el sistema real. El modelo solo clasifica la longitud por tramos y no calcula itinerarios, duración, tarifas, transbordos reales ni condiciones de operación.
