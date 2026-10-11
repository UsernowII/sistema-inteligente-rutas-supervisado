# Clasificador supervisado de longitud de rutas

Aplicación de consola en Python que entrena un árbol de decisión para clasificar un viaje en la red académica simplificada de TransMilenio como **corto**, **medio** o **largo**.

## Datos y modelo

No se suministraron registros reales de viajes, pasajeros ni tiempos del sistema de transporte. Por eso, el proyecto crea un dataset sintético a partir de las nueve estaciones y ocho conexiones de la actividad 2. Incluye los 72 pares ordenados posibles de estaciones distintas. La cantidad de tramos de cada par se obtiene buscando una ruta mínima en la red simplificada.

La clase objetivo se define así: corta (1–2 tramos), media (3–4) y larga (5 o más). El árbol recibe como características los índices de origen y destino y la diferencia entre ambos índices. `segments` queda en el CSV para describir y comprobar la etiqueta; no se usa como entrada del modelo.

El programa separa los datos de forma estratificada: 53 ejemplos para entrenar y 19 para probar. Entrena un árbol de decisión pequeño usando impureza Gini y muestra su exactitud en esa partición. Es una demostración académica con datos sintéticos: no estima tiempos reales, no encuentra la ruta exacta y su exactitud no debe interpretarse como rendimiento sobre viajes reales.

## Continuidad con la actividad 2

La actividad 2 responde: **¿qué camino conecta estas dos estaciones con la menor cantidad de tramos?** Para eso recorre la red con BFS (búsqueda en anchura) y devuelve la secuencia de estaciones. En este proyecto conservamos esa red y usamos BFS para calcular los tramos de los ejemplos sintéticos. Después, el árbol de decisión aprende a clasificar la longitud del viaje como corta, media o larga. Por tanto, este modelo supervisado no reemplaza BFS ni predice la ruta exacta: aprende una categoría a partir de ejemplos que ya tienen etiqueta.

## Requisitos

- Python 3.
- No se necesitan paquetes externos ni conexión a internet.

## Ejecutar

Desde la carpeta del proyecto:

```bash
python main.py
```

En macOS o Linux, puedes usar `python3 main.py` si `python` no está disponible. Ingresa una estación de origen y una de destino cuando el programa las solicite.

Para regenerar el archivo CSV desde la base de conocimiento:

```bash
python generate_dataset.py
```

Para ejecutar las pruebas:

```bash
python -m unittest -v
```

En macOS o Linux también puedes anteponer `python3` a esos comandos.

## Archivos

- `knowledge_base.py`: estaciones y conexiones de la red académica simplificada.
- `generate_dataset.py`: genera los viajes y etiquetas sintéticas a partir de la red.
- `data/trips_simplified.csv`: dataset entregado con 72 pares origen-destino.
- `decision_tree.py`: carga datos, separa entrenamiento/prueba, calcula Gini y entrena y evalúa el árbol.
- `main.py`: entrena el modelo, muestra la evaluación y solicita un viaje para clasificar.
- `test_supervised_model.py`: pruebas automatizadas con `unittest`.
- `data_description.md`: procedencia, campos y limitaciones del dataset.
- `test_results.md`: casos y resultados de las pruebas.
- `mapa_conceptual.md`: mapa conceptual del proceso supervisado.

## Alcance

La red y el dataset son muestras didácticas derivadas de la actividad anterior, no datos oficiales ni observaciones del servicio actual. La clasificación depende de los límites definidos para las clases. Para un modelo aplicable al transporte real se necesitarían datos representativos y verificados de viajes, horarios, distancias o tiempos.
