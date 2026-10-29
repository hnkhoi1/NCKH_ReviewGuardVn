# Data policy

This repository is **public**. Anything pushed here is visible to everyone and stays in the git history.

## Never commit

- Raw or scraped reviews, or any file derived from them that still contains review text
- Reviewer names, ids, profile links, phone numbers or other personal data
- API keys, tokens, passwords, `.env` files
- Model weights and MLflow databases

## How we handle data

1. **Collection**: public pages only, rate-limited scripts, within each platform's terms of use.
2. **Anonymisation**: reviewer ids are removed or replaced by a salted hash before any sharing.
3. **Sharing inside the team**: private drive or direct transfer; record the download location in `data/README.md`
   (without credentials).
4. **Third-party datasets** (for example ViSpamReviews): check the licence and terms on the dataset page before use or
   redistribution; cite the original paper.
5. **Outputs** of the system are suspicion indicators for human review, not accusations against any person or seller.

## If something sensitive was pushed by mistake

Tell the other member immediately. Deleting the file in a later commit is not enough because history keeps it;
the history must be rewritten and any exposed credential must be revoked.
