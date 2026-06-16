import os
import sys

from datetime import datetime
import pandas as pd

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from providers.mock_provider import MockProvider

WATCHLIST_PATH = os.path.join(
    "pipelines",
    "watchlist.csv"
)

SNAPSHOT_DIR = os.path.join(
    "pipelines",
    "snapshots"
)


def load_watchlist() -> list:
    """
    Load monitoring keywords from watchlist.csv.
    """

    watchlist = pd.read_csv(
        WATCHLIST_PATH
    )

    return (
        watchlist["keyword"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )


def run_ingestion_pipeline(
    provider=None,
    limit: int = 20
) -> pd.DataFrame:
    """
    Execute the market ingestion pipeline.

    Flow:
    watchlist
        ↓
    provider
        ↓
    snapshots
        ↓
    combined dataframe
    """

    if provider is None:

        provider = MockProvider()

    os.makedirs(
        SNAPSHOT_DIR,
        exist_ok=True
    )

    keywords = load_watchlist()

    all_data = []

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    for keyword in keywords:

        try:

            products = (
                provider.fetch_products(
                    keyword=keyword,
                    limit=limit
                )
            )

            snapshot_filename = (
                f"{current_date}_"
                f"{keyword.lower().replace(' ', '_')}.csv"
            )

            snapshot_path = os.path.join(
                SNAPSHOT_DIR,
                snapshot_filename
            )

            products.to_csv(
                snapshot_path,
                index=False
            )

            all_data.append(
                products
            )

            print(
                f"✓ Snapshot saved: "
                f"{snapshot_filename}"
            )

        except Exception as e:

            print(
                f"✗ Failed for "
                f"{keyword}: {e}"
            )

    if len(all_data) == 0:

        return pd.DataFrame()

    return pd.concat(
        all_data,
        ignore_index=True
    )


if __name__ == "__main__":

    result = run_ingestion_pipeline()

    print("\nPipeline Completed")

    print(
        f"Total Products: "
        f"{len(result)}"
    )

    print(
        result.head()
    )