"""Base de conocimiento simplificada reutilizada de la actividad 2."""

import unicodedata


# Hechos académicos: estaciones y conexiones bidireccionales.
CONNECTIONS = {
    "Portal Norte": ["Calle 100"],
    "Calle 100": ["Portal Norte", "Calle 72"],
    "Calle 72": ["Calle 100", "Héroes"],
    "Héroes": ["Calle 72", "Calle 26"],
    "Calle 26": ["Héroes", "Museo Nacional", "Ricaurte"],
    "Museo Nacional": ["Calle 26"],
    "Ricaurte": ["Calle 26", "Portal Américas"],
    "Portal Américas": ["Ricaurte", "Bosa"],
    "Bosa": ["Portal Américas"],
}

STATIONS = list(CONNECTIONS)


def normalize_station_name(station):
    """Normaliza espacios, mayúsculas y tildes para comparar estaciones."""
    normalized = " ".join(station.strip().split()).casefold()
    decomposed = unicodedata.normalize("NFD", normalized)
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def get_canonical_station(station):
    """Retorna el nombre oficial de una estación o None si no se encuentra."""
    if not isinstance(station, str):
        return None

    normalized = normalize_station_name(station)
    for official_station in STATIONS:
        if normalize_station_name(official_station) == normalized:
            return official_station
    return None


def get_neighbors(station):
    """Retorna las estaciones conectadas con la estación indicada."""
    official_station = get_canonical_station(station)
    if official_station is None:
        return []
    return list(CONNECTIONS.get(official_station, []))


def get_stations():
    """Retorna una copia de las estaciones disponibles."""
    return list(STATIONS)
