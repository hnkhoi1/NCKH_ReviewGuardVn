# Contributing

This project has two members, so the workflow is deliberately light.

## Branches

- `main` always runs. Do not push broken code to it.
- Work on a short-lived branch and open a pull request (PR) for the other member to review:
  - `feature/<topic>` for new code (example: `feature/phobert-finetune`)
  - `fix/<topic>` for bug fixes
  - `docs/<topic>` for documentation and literature notes
- Update your branch before opening a PR: `git pull origin main`.

## Commits

Small commits with a short imperative message:

```text
Add TF-IDF baseline config
Fix group split when product_id is missing
Document MLflow naming convention
```

## Experiments

1. Create or copy a config in `configs/` (one config per experiment, never edit a config after a result was reported).
2. Run it with a script from `scripts/`.
3. Check the run in the MLflow UI. If a result goes into the report, note the run name in the PR description.

## Before opening a PR

- [ ] `pytest` passes
- [ ] No data files, model weights, tokens or `.env` files are staged (`git status`)
- [ ] README or docs updated if behaviour changed

## Windows tips

- Run `git config --global core.autocrlf true` once, so line endings do not create noisy diffs.
- If a command fails with "running scripts is disabled", see the PowerShell note in the README.
