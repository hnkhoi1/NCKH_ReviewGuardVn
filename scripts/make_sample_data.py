"""Create a tiny SYNTHETIC review dataset for smoke tests. It contains no real reviews."""
import os
import random

import pandas as pd

random.seed(0)

GENUINE = [
    "May dung on, pin trau, giao hang hoi cham nhung dong goi can than",
    "Mau hoi khac anh mot chut nhung chat luong tam on voi gia tien",
    "Mua lan thu hai, lan nay tay ao vua hon, se mua them size khac",
    "San pham dung nhu mo ta, dung duoc 2 tuan thay on dinh",
    "Giao dung hen, shop tu van nhiet tinh, loa nghe duoc",
    "Chat vai mem, mac mat, nhung duong chi can chinh them",
]
TEMPLATES = [
    "San pham tuyet voi, shop uy tin, nhat dinh se ung ho dai dai, 5 sao",
    "Hang dep chat luong, giao hang sieu nhanh, rat hai long, 5 sao",
    "Shop dong goi ky, tu van nhiet tinh, san pham tot, nen mua",
]

rows = []
rid = 0
for p in range(40):
    suspicious_product = p % 4 == 0
    for _ in range(random.randint(8, 14)):
        rid += 1
        if suspicious_product and random.random() < 0.7:
            text = random.choice(TEMPLATES) + random.choice(["", " !!!", " ngay"])
            rows.append((rid, f"P{p:03d}", text, 5, 1))
        else:
            rows.append((rid, f"P{p:03d}", random.choice(GENUINE), random.choice([3, 4, 4, 5]), 0))

df = pd.DataFrame(rows, columns=["review_id", "product_id", "text", "rating", "label"])
os.makedirs("data/sample", exist_ok=True)
df.to_csv("data/sample/synthetic_reviews.csv", index=False)
print(f"Wrote data/sample/synthetic_reviews.csv with {len(df)} synthetic rows "
      f"({df.label.mean():.0%} suspicious)")
