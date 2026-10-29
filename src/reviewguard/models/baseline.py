"""Content-based baselines."""
from __future__ import annotations

from typing import Any, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_tfidf_logreg(cfg: Dict[str, Any], seed: int = 42) -> Pipeline:
    """TF-IDF (word or character n-grams) followed by Logistic Regression."""
    tfidf_cfg = cfg["tfidf"]
    model_cfg = cfg["model"]
    vectorizer = TfidfVectorizer(
        analyzer=tfidf_cfg.get("analyzer", "char_wb"),
        ngram_range=tuple(tfidf_cfg.get("ngram_range", [2, 5])),
        min_df=tfidf_cfg.get("min_df", 1),
        max_features=tfidf_cfg.get("max_features"),
        sublinear_tf=tfidf_cfg.get("sublinear_tf", True),
        lowercase=tfidf_cfg.get("lowercase", True),
    )
    classifier = LogisticRegression(
        C=model_cfg.get("C", 1.0),
        class_weight=model_cfg.get("class_weight"),
        max_iter=model_cfg.get("max_iter", 1000),
        random_state=seed,
    )
    return Pipeline([("tfidf", vectorizer), ("clf", classifier)])
