# Pruebas del componente de aprendizaje supervisado

Las pruebas se ejecutan desde la carpeta del proyecto con:

```bash
python -m unittest -v
```

En macOS o Linux puede usarse `python3 -m unittest -v`.

| # | Caso | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| 1 | Límites de las clases para 2, 3 y 5 tramos | corta, media y larga respectivamente | corta, media y larga | Aprobada |
| 2 | Generación de filas para pares ordenados distintos | 72 filas y ningún origen igual al destino | 72 filas; no hay pares consigo mismos | Aprobada |
| 3 | Lectura del CSV | 72 muestras con etiquetas válidas | 72 muestras cargadas; etiquetas corta, media o larga | Aprobada |
| 4 | División estratificada | 53 de entrenamiento y 19 de prueba, con las tres clases | 53 y 19; ambas particiones contienen las tres clases | Aprobada |
| 5 | Aprendizaje de patrón controlado | árbol predice las dos clases del ejemplo correctamente | exactitud 100% en el ejemplo de prueba pequeño | Aprobada |
| 6 | Entrenamiento y evaluación del dataset de rutas | predicción dentro de las clases definidas y exactitud válida | 84,2% (16 de 19) en la partición sintética fija | Aprobada |

## Conclusión

Las seis pruebas automatizadas finalizaron correctamente (`Ran 6 tests`, `OK`). En la partición estratificada con semilla 42, el árbol de decisión clasificó correctamente 16 de los 19 ejemplos de prueba (84,2%). Esta cifra describe únicamente esta muestra sintética y pequeña; no debe presentarse como exactitud esperada en viajes reales.
