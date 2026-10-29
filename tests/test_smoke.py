"""Smoke tests: data split has no group leakage and metrics are computed."""
import pandas as pd

from reviewguard.data import split_data
from reviewguard.evaluation.metrics import binary_metrics


def make_df():
    rows = []
    for p in range(10):
        for i in range(6):
            rows.append({"product_id": f"P{p}", "text": f"review {p} {i}", "label": int((p + i) % 3 == 0)})
    return pd.DataFrame(rows)


def test_group_split_has_no_overlap():
    df = make_df()
    train, test = split_data(df, "label", group_col="product_id", test_size=0.3, seed=1)
    assert set(train.product_id).isdisjoint(set(test.product_id))
    assert len(train) + len(test) == len(df)


def test_binary_metrics_keys():
    metrics = binary_metrics([0, 1, 1, 0], [0, 1, 0, 0], [0.1, 0.9, 0.4, 0.2])
    assert {"precision", "recall", "f1", "f1_macro", "pr_auc", "roc_auc"} <= set(metrics)
    assert metrics["precision"] == 1.0
