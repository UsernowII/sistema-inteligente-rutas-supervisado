"""Árbol de decisión de clasificación implementado con Python estándar."""

import csv
import random
from collections import Counter, defaultdict


def load_samples(csv_path):
    """Lee filas CSV y devuelve pares (características, etiqueta)."""
    samples = []
    with open(csv_path, "r", newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            features = (
                int(row["origin_index"]),
                int(row["destination_index"]),
                int(row["order_gap"]),
            )
            samples.append((features, row["route_class"]))
    return samples


def stratified_split(samples, test_fraction=0.25, seed=42):
    """Separa datos por etiqueta para conservar sus proporciones en prueba."""
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction debe estar entre 0 y 1.")

    groups = defaultdict(list)
    for sample in samples:
        groups[sample[1]].append(sample)

    randomizer = random.Random(seed)
    train_samples = []
    test_samples = []

    for label in sorted(groups):
        group = list(groups[label])
        randomizer.shuffle(group)
        test_count = max(1, int(len(group) * test_fraction + 0.5))
        test_count = min(test_count, len(group) - 1)
        test_samples.extend(group[:test_count])
        train_samples.extend(group[test_count:])

    randomizer.shuffle(train_samples)
    randomizer.shuffle(test_samples)
    return train_samples, test_samples


def gini_impurity(labels):
    """Calcula la impureza Gini de un grupo de etiquetas."""
    if not labels:
        return 0.0

    counts = Counter(labels)
    total = len(labels)
    return 1.0 - sum((count / total) ** 2 for count in counts.values())


def _majority_label(labels):
    counts = Counter(labels)
    return sorted(counts, key=lambda label: (-counts[label], label))[0]


def _best_split(samples):
    labels = [label for _, label in samples]
    parent_impurity = gini_impurity(labels)
    best_candidate = None

    for feature_index in range(len(samples[0][0])):
        values = sorted({features[feature_index] for features, _ in samples})
        thresholds = [(left + right) / 2 for left, right in zip(values, values[1:])]

        for threshold in thresholds:
            left_samples = [
                sample for sample in samples if sample[0][feature_index] <= threshold
            ]
            right_samples = [
                sample for sample in samples if sample[0][feature_index] > threshold
            ]
            if not left_samples or not right_samples:
                continue

            weighted_impurity = (
                len(left_samples) * gini_impurity([label for _, label in left_samples])
                + len(right_samples) * gini_impurity([label for _, label in right_samples])
            ) / len(samples)
            gain = parent_impurity - weighted_impurity

            if best_candidate is None or gain > best_candidate["gain"]:
                best_candidate = {
                    "feature_index": feature_index,
                    "threshold": threshold,
                    "gain": gain,
                    "left": left_samples,
                    "right": right_samples,
                }

    return best_candidate


def _build_tree(samples, depth, max_depth):
    labels = [label for _, label in samples]
    prediction = _majority_label(labels)

    if len(set(labels)) == 1 or depth >= max_depth or len(samples) < 2:
        return {"prediction": prediction}

    split = _best_split(samples)
    if split is None or split["gain"] <= 0:
        return {"prediction": prediction}

    return {
        "feature_index": split["feature_index"],
        "threshold": split["threshold"],
        "left": _build_tree(split["left"], depth + 1, max_depth),
        "right": _build_tree(split["right"], depth + 1, max_depth),
    }


def train_decision_tree(samples, max_depth=2):
    """Entrena recursivamente un árbol que predice la clase de longitud."""
    if not samples:
        raise ValueError("No hay ejemplos para entrenar el modelo.")
    if max_depth < 1:
        raise ValueError("max_depth debe ser al menos 1.")
    return _build_tree(samples, depth=0, max_depth=max_depth)


def predict(tree, features):
    """Predice la etiqueta de un par de características usando el árbol."""
    current_node = tree
    while "prediction" not in current_node:
        feature_value = features[current_node["feature_index"]]
        if feature_value <= current_node["threshold"]:
            current_node = current_node["left"]
        else:
            current_node = current_node["right"]
    return current_node["prediction"]


def accuracy(tree, samples):
    """Retorna la proporción de predicciones correctas para un conjunto."""
    if not samples:
        return 0.0
    correct = sum(predict(tree, features) == label for features, label in samples)
    return correct / len(samples)
