# Mapa conceptual: aprendizaje supervisado para clasificar rutas

```mermaid
flowchart TD
    A[Sistema inteligente de rutas para una red simplificada de TransMilenio] --> B[Hechos de estaciones y conexiones]
    B --> C[Generador de viajes sintéticos]
    C --> D[Dataset CSV: 72 pares origen-destino]
    D --> E[Características: índice origen, índice destino y diferencia]
    D --> F[Etiqueta objetivo: corta, media o larga]
    E --> G[Separación estratificada]
    F --> G
    G --> H[53 ejemplos para entrenar]
    G --> I[19 ejemplos para probar]
    H --> J[Árbol de decisión supervisado]
    J --> K[Predicción de clase de longitud]
    I --> L[Evaluación: exactitud]
    J --> L
    M[Datos sintéticos; no son viajes reales] -. limita .-> D
    N[Cada conexión cuenta como un tramo] --> F
```

El mapa muestra cómo los hechos de la red se convierten en ejemplos etiquetados; el árbol aprende de una parte de los ejemplos y se evalúa con otra parte que no se usó para entrenarlo.
