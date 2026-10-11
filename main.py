"""Entrena el árbol de decisión y predice la longitud de una ruta."""

from pathlib import Path

from decision_tree import accuracy, load_samples, predict, stratified_split, train_decision_tree
from knowledge_base import get_canonical_station, get_stations


DATA_PATH = Path(__file__).resolve().parent / "data" / "trips_simplified.csv"
ROUTE_CLASS_NAMES = {
    "corta": "corta (hasta 2 tramos)",
    "media": "media (de 3 a 4 tramos)",
    "larga": "larga (5 o más tramos)",
}


def main():
    samples = load_samples(DATA_PATH)
    train_samples, test_samples = stratified_split(samples)
    model = train_decision_tree(train_samples, max_depth=2)
    model_accuracy = accuracy(model, test_samples)
    station_indexes = {station: index for index, station in enumerate(get_stations())}

    print("Clasificador de longitud de rutas - red simplificada de TransMilenio")
    print("Modelo: árbol de decisión supervisado")
    print("Ejemplos de entrenamiento: {}".format(len(train_samples)))
    print("Ejemplos de prueba: {}".format(len(test_samples)))
    print("Exactitud en los datos de prueba: {:.1%}".format(model_accuracy))
    print("\nEstaciones disponibles:")
    print(", ".join(get_stations()))

    origin_input = input("\nIngrese la estación de origen: ")
    destination_input = input("Ingrese la estación de destino: ")
    origin = get_canonical_station(origin_input)
    destination = get_canonical_station(destination_input)

    if origin is None:
        print("\nError: la estación de origen no existe en este ejercicio.")
        return
    if destination is None:
        print("\nError: la estación de destino no existe en este ejercicio.")
        return
    if origin == destination:
        print("\nEl origen y el destino son la misma estación; no se necesita un trayecto.")
        return

    origin_index = station_indexes[origin]
    destination_index = station_indexes[destination]
    features = (
        origin_index,
        destination_index,
        abs(origin_index - destination_index),
    )
    predicted_class = predict(model, features)

    print("\nPredicción del modelo: ruta {}.".format(ROUTE_CLASS_NAMES[predicted_class]))
    print("Esta predicción clasifica la longitud; no calcula la ruta exacta ni el tiempo real.")


if __name__ == "__main__":
    main()
