"""Train and evaluate the TF-IDF + Logistic Regression baseline, logging everything to MLflow.

Usage:
    python scripts/train_baseline.py --config configs/baseline_tfidf_lr.yaml
"""
import argparse

import mlflow
import yaml

from reviewguard.data import load_reviews, split_data
from reviewguard.evaluation.metrics import binary_metrics
from reviewguard.models.baseline import build_tfidf_logreg
from reviewguard.tracking import tracked_run


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to a YAML config")
    parser.add_argument("--run-name", default=None, help="Override run_name from the config")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)

    data_cfg = cfg["data"]
    seed = data_cfg.get("seed", 42)
    text_col, label_col = data_cfg["text_col"], data_cfg["label_col"]
    group_col = data_cfg.get("group_col")

    df = load_reviews(data_cfg["path"], text_col, label_col, group_col)
    train, test = split_data(df, label_col, group_col, data_cfg.get("test_size", 0.2), seed)
    if test[label_col].nunique() < 2:
        raise SystemExit("The test split contains a single class; change seed/test_size or add more data.")

    run_name = args.run_name or cfg.get("run_name")
    with tracked_run(
        experiment=cfg["experiment"],
        run_name=run_name,
        params=cfg,
        data_path=data_cfg["path"],
        config_path=args.config,
    ):
        model = build_tfidf_logreg(cfg, seed=seed)
        model.fit(train[text_col], train[label_col])

        pred = model.predict(test[text_col])
        score = model.predict_proba(test[text_col])[:, 1]
        metrics = binary_metrics(test[label_col], pred, score)

        mlflow.log_params({"n_train": len(train), "n_test": len(test),
                           "positive_rate_train": round(float(train[label_col].mean()), 4)})
        mlflow.log_metrics(metrics)

    print("Run finished. Metrics:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")


if __name__ == "__main__":
    main()
