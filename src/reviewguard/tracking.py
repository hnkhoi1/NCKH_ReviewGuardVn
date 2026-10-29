"""Thin MLflow helper so every run records the same provenance information."""
from __future__ import annotations

import contextlib
import hashlib
import os
import subprocess
from typing import Any, Dict, Iterator, Optional

import mlflow

DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"


def git_commit() -> str:
    """Return the current git commit hash, or ``unknown`` outside a git repository."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def sha256_file(path: str) -> str:
    """SHA-256 of a file, used as a cheap data version."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """Flatten a nested dict into dotted keys (MLflow params are flat)."""
    flat: Dict[str, Any] = {}
    for key, value in d.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            flat.update(flatten(value, prefix=name + "."))
        else:
            flat[name] = value
    return flat


@contextlib.contextmanager
def tracked_run(
    experiment: str,
    run_name: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    data_path: Optional[str] = None,
    config_path: Optional[str] = None,
) -> Iterator["mlflow.ActiveRun"]:
    """Start an MLflow run and log code version, data hash, config and parameters."""
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", DEFAULT_TRACKING_URI))
    mlflow.set_experiment(experiment)
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.set_tag("git_commit", git_commit())
        if data_path and os.path.exists(data_path):
            mlflow.set_tag("data_sha256", sha256_file(data_path))
            mlflow.set_tag("data_path", data_path)
        if params:
            mlflow.log_params({k: str(v) for k, v in flatten(params).items()})
        if config_path and os.path.exists(config_path):
            mlflow.log_artifact(config_path)
        yield run
