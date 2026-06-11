import os
from datetime import datetime

import pandas as pd

from database import supabase


SNAPSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "pipelines",
    "snapshots"
)

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


KEYWORDS = [
    "protein powder",
    "running shoes",
    "wireless earbuds"
]


def collect_market_snapshots():

    print("\nCollecting daily snapshots...")

    today = str(datetime.now().date())

    total_rows = 0

    for keyword in KEYWORDS:

        response = (
            supabase
            .table("market_products")
            .select("*")
            .eq("keyword", keyword)
            .execute()
        )

        if not response.data:

            print(f"No data found for {keyword}")
            continue

        df = pd.DataFrame(response.data)

        if df.empty:
            continue

        df["timestamp"] = datetime.now().isoformat()

        filename = os.path.join(
            SNAPSHOT_DIR,
            f"{today}_{keyword.replace(' ', '_')}.csv"
        )

        df[
            [
                "keyword",
                "product_name",
                "price",
                "rating",
                "review_count",
                "timestamp"
            ]
        ].to_csv(
            filename,
            index=False
        )

        total_rows += len(df)

        print(
            f"✓ {keyword}: "
            f"{len(df)} rows saved"
        )

    print(
        f"\nSnapshots completed."
        f"\nTotal rows: {total_rows}"
    )


if __name__ == "__main__":

    collect_market_snapshots()