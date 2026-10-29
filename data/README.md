# Data folder

Everything in `raw/`, `interim/`, `processed/` and `external/` is ignored by git (only `.gitkeep` files are tracked).

| Folder | Content |
|---|---|
| `raw/` | Data exactly as collected (scraped reviews, downloaded datasets) |
| `interim/` | Cleaned or partly processed data |
| `processed/` | Final train / validation / test splits |
| `external/` | Third-party datasets (for example ViSpamReviews) |
| `sample/` | Tiny **synthetic** sample used only for smoke tests (tracked by git) |

## Expected CSV columns

| Column | Meaning |
|---|---|
| `review_id` | Unique id of the review |
| `product_id` | Product or shop id (used for group-wise splitting) |
| `text` | Review text |
| `rating` | Star rating (1–5), if available |
| `label` | 0 = trustworthy, 1 = suspicious |

Optional columns when available: `posted_at`, `reviewer_hash` (hashed, never the raw reviewer id), `platform`, `category`.

See [../docs/DATA_POLICY.md](../docs/DATA_POLICY.md) before adding any data.
