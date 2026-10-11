"""Pruebas del dataset y del clasificador supervisado."""

import unittest
from pathlib import Path

from decision_tree import accuracy, load_samples, predict, stratified_split, train_decision_tree
from generate_dataset import build_dataset_rows, classify_route_length


PROJECT_PATH = Path(__file__).resolve().parent
DATA_PATH = PROJECT_PATH / "data" / "trips_simplified.csv"


class SupervisedModelTests(unittest.TestCase):
    def test_route_length_classes(self):
        self.assertEqual(classify_route_length(2), "corta")
        self.assertEqual(classify_route_length(3), "media")
        self.assertEqual(classify_route_length(5), "larga")

    def test_dataset_has_one_row_per_ordered_distinct_station_pair(self):
        rows = build_dataset_rows()
        self.assertEqual(len(rows), 9 * 8)
        self.assertTrue(all(row["origin"] != row["destination"] for row in rows))

    def test_csv_dataset_can_be_loaded(self):
        samples = load_samples(DATA_PATH)
        self.assertEqual(len(samples), 72)
        self.assertTrue(all(label in {"corta", "media", "larga"} for _, label in samples))

    def test_split_is_reproducible_and_keeps_all_labels(self):
        samples = load_samples(DATA_PATH)
        train_samples, test_samples = stratified_split(samples)
        self.assertEqual((len(train_samples), len(test_samples)), (53, 19))
        self.assertEqual(set(label for _, label in train_samples), {"corta", "media", "larga"})
        self.assertEqual(set(label for _, label in test_samples), {"corta", "media", "larga"})

    def test_tree_learns_a_simple_supervised_pattern(self):
        samples = [((value,), "corta" if value <= 2 else "larga") for value in range(8)]
        model = train_decision_tree(samples, max_depth=2)
        self.assertEqual(predict(model, (1,)), "corta")
        self.assertEqual(predict(model, (6,)), "larga")
        self.assertEqual(accuracy(model, samples), 1.0)

    def test_route_model_returns_a_known_class(self):
        samples = load_samples(DATA_PATH)
        train_samples, test_samples = stratified_split(samples)
        model = train_decision_tree(train_samples)
        self.assertGreaterEqual(accuracy(model, test_samples), 0.75)
        self.assertLessEqual(accuracy(model, test_samples), 1.0)
        self.assertIn(predict(model, (0, 7, 7)), {"corta", "media", "larga"})


if __name__ == "__main__":
    unittest.main()
