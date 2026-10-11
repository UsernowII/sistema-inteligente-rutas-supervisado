"""Genera viajes sintéticos a partir de la red simplificada de estaciones."""

import csv
from collections import deque
from pathlib import Path

from knowledge_base import get_neighbors, get_stations


DATA_PATH = Path(__file__).resolve().parent / "data" / "trips_simplified.csv"
CSV_FIELDS = (
    "origin",
    "destination",
    "origin_index",
    "destination_index",
    "order_gap",
    "segments",
    "route_class",
)


def shortest_route_segments(origin, destination):
    """Cuenta los tramos de la ruta más corta entre dos estaciones conocidas."""
    queue = deque([(origin, 0)])
    visited = {origin}

    while queue:
        current_station, segments = queue.popleft()
        if current_station == destination:
            return segments

        for neighbor in get_neighbors(current_station):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, segments + 1))

    return None


def classify_route_length(segments):
    """Asigna la etiqueta didáctica de longitud según el número de tramos."""
    if segments <= 2:
        return "corta"
    if segments <= 4:
        return "media"
    return "larga"


def build_dataset_rows():
    """Crea una fila sintética para cada par ordenado de estaciones distintas."""
    stations = get_stations()
    station_indexes = {station: index for index, station in enumerate(stations)}
    rows = []

    for origin in stations:
        for destination in stations:
            if origin == destination:
                continue

            segments = shortest_route_segments(origin, destination)
            if segments is None:
                continue

            rows.append(
                {
                    "origin": origin,
                    "destination": destination,
                    "origin_index": station_indexes[origin],
                    "destination_index": station_indexes[destination],
                    "order_gap": abs(station_indexes[origin] - station_indexes[destination]),
                    "segments": segments,
                    "route_class": classify_route_length(segments),
                }
            )

    return rows


def write_dataset(output_path=DATA_PATH):
    """Escribe el conjunto sintético en un archivo CSV y retorna sus filas."""
    rows = build_dataset_rows()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    return rows


if __name__ == "__main__":
    generated_rows = write_dataset()
    print("Dataset sintético creado con {} viajes.".format(len(generated_rows)))
    print("Archivo: {}".format(DATA_PATH))
