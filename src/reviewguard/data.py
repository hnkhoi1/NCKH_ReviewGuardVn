"""Loading and splitting review data."""
from __future__ import annotations

from typing import Optional, Tuple

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split


def load_reviews(
    path: str,
    text_col: str = "text",
    label_col: str = "label",
    group_col: Optional[str] = None,
) -> pd.DataFrame:
    """Read a CSV of reviews and validate the required columns."""
    df = pd.read_csv(path)
    required = [text_col, label_col] + ([group_col] if group_col else [])
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")
    df = df.dropna(subset=[text_col, label_col]).copy()
    df[text_col] = df[text_col].astype(str)
    df[label_col] = df[label_col].astype(int)
    return df.reset_index(drop=True)


def split_data(
    df: pd.DataFrame,
    label_col: str = "label",
    group_col: Optional[str] = None,
    test_size: float = 0.2,
    seed: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split into train/test.

    If ``group_col`` is given (product or shop id), whole groups go to one side only, which avoids leakage between
    near-duplicate reviews of the same product.
    """
    if group_col:
        splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
        train_idx, test_idx = next(splitter.split(df, df[label_col], groups=df[group_col]))
        return df.iloc[train_idx].reset_index(drop=True), df.iloc[test_idx].reset_index(drop=True)
    train, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=df[label_col])
    return train.reset_index(drop=True), test.reset_index(drop=True)
