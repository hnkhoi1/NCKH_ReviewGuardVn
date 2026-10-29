# ReviewGuard VN

**Detecting deceptive reviews and suspicious review patterns in Vietnamese e-commerce.**

Student scientific research (NCKH) project, academic year 2026–2027.

ReviewGuard VN decides whether a Vietnamese e-commerce review is trustworthy or suspicious by combining
two sources of evidence, and explains its decision:

| Branch | Question it answers | Main techniques |
|---|---|---|
| Content branch | Does the text of this review look untrustworthy? | TF-IDF baselines, fine-tuned PhoBERT / XLM-R, LLM few-shot prompting |
| Pattern branch | Does this review behave like part of a suspicious group? | Sentence embeddings, cosine similarity, HDBSCAN, burst score, Isolation Forest, community detection |
| Fusion | How do the two signals combine? | Stacking meta-classifier |
| Explanation | Why was it flagged? | SHAP, similar-review clusters, reason codes, web demo |

## Status

This repository currently holds the project skeleton (October 2026 milestone). Model code is added step by step
following the schedule in the research proposal.

- [x] Repository skeleton and experiment tracking
- [ ] Literature survey and taxonomy of untrustworthy reviews
- [ ] Data collection and annotation guideline
- [ ] Baselines (TF-IDF + linear models)
- [ ] Transformer models (PhoBERT, XLM-R)
- [ ] Review-pattern analysis (embeddings, clustering, anomaly detection)
- [ ] Fusion model and evaluation
- [ ] Explainable web demo

## Repository layout

```text
NCKH_ReviewGuardVn/
├── README.md                  Project overview and setup (this file)
├── CONTRIBUTING.md            Git workflow and conventions
├── requirements.txt           Core dependencies
├── requirements-ml.txt        Heavy ML dependencies (transformers, SHAP, Streamlit, ...)
├── pyproject.toml             Makes `src/reviewguard` installable (pip install -e .)
├── configs/                   One YAML file per experiment
├── data/                      Local data only; never committed (see docs/DATA_POLICY.md)
│   └── sample/                Tiny synthetic sample used for smoke tests
├── docs/                      Experiment tracking guide, data policy, literature review
├── notebooks/                 Exploratory notebooks
├── scripts/                   Command-line entry points (train, make sample data, ...)
├── src/reviewguard/           Python package
│   ├── data.py                Loading and splitting (split by product/shop to avoid leakage)
│   ├── tracking.py            MLflow helper: every run logs params, metrics, git commit, data hash
│   ├── models/                Content-based classifiers
│   ├── patterns/              Review-pattern analysis (placeholder)
│   ├── evaluation/            Metrics
│   └── explain/               Explanations (placeholder)
├── app/                       Web demo (placeholder)
└── tests/                     Smoke tests
```

## Quick start (Windows, PowerShell)

Requirements: [Git for Windows](https://git-scm.com/download/win) and Python 3.10 or newer from python.org
(tick "Add python.exe to PATH" and keep the `py` launcher).

```powershell
git clone https://github.com/hnkhoi1/NCKH_ReviewGuardVn.git
cd NCKH_ReviewGuardVn

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

If PowerShell refuses to run `Activate.ps1`, run this once and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Run the smoke test

```powershell
python scripts/make_sample_data.py
python scripts/train_baseline.py --config configs/baseline_tfidf_lr.yaml
pytest
```

### Look at the results

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open <http://127.0.0.1:5000>. Each run shows its parameters, metrics, git commit and a hash of the data file.
See [docs/EXPERIMENT_TRACKING.md](docs/EXPERIMENT_TRACKING.md) for the conventions.

### Heavy dependencies (transformers, PyTorch, SHAP, Streamlit)

Install PyTorch first by choosing your CPU/GPU build on <https://pytorch.org/get-started/locally/>, then:

```powershell
pip install -r requirements-ml.txt
```

## Data

The repository is public. **Do not commit raw reviews, scraped files, reviewer identifiers or credentials.**
Keep data in the local `data/` folders (ignored by git) and share it through the team's private drive.
Details: [docs/DATA_POLICY.md](docs/DATA_POLICY.md).

## Working together

Short-lived branches, pull requests reviewed by the other member, one experiment config per run.
Details: [CONTRIBUTING.md](CONTRIBUTING.md).

## Key references

The full list is in the research proposal; the main sources behind this design are Jindal & Liu (2008),
Mukherjee et al. (2012), Rayana & Akoglu (2015), Salminen et al. (2022), PhoBERT (Nguyen & Nguyen, 2020),
Sentence-BERT (Reimers & Gurevych, 2019), HDBSCAN (McInnes et al., 2017), Isolation Forest (Liu et al., 2008)
and SHAP (Lundberg & Lee, 2017). A structured summary is kept in [docs/literature](docs/literature/README.md).

## License

To be decided by the team (no license file yet, so all rights are reserved by default).
