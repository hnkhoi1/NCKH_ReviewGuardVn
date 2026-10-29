# Experiment tracking

All experiments are logged with [MLflow](https://mlflow.org/) into a local SQLite database (`mlflow.db`, ignored by git).

## Why

The project compares baselines, improved models and ablations. Without a record of which data, parameters and code
produced each number, results cannot be compared or reproduced.

## What every run logs

| Item | How |
|---|---|
| Parameters | Flattened config (model, TF-IDF settings, seed, split) |
| Metrics | Precision, Recall, F1 (suspicious class and macro), PR-AUC, ROC-AUC |
| Code version | `git_commit` tag |
| Data version | SHA-256 hash of the data file (`data_sha256`) |
| Config file | Stored as an artifact |

`src/reviewguard/tracking.py` does this automatically; new scripts should use `tracked_run(...)`.

## Naming convention

- Experiment (one per question): `baseline-content`, `pattern-clustering`, `fusion`, `robustness-llm-generated`
- Run name: `<model>-<dataset>-<short-note>`, for example `phobert-selfcollected-lr2e5`

## Typical commands

```powershell
python scripts/train_baseline.py --config configs/baseline_tfidf_lr.yaml
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Compare runs in the UI: select several runs, then **Compare**.

## Rules

1. Never change a config after its result was reported; copy it to a new file instead.
2. Always split by product or shop (`group_col`) so near-duplicate reviews do not leak between train and test.
3. Report the same metrics for every model so tables stay comparable.
4. Record the run name in the pull request when a number goes into the report.
