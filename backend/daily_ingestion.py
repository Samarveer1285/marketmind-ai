import os
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Resolve backend/.env relative to this file, not the process's current working
# directory, so this script behaves the same whether it's launched from the repo
# root, from backend/, or (soon) from a GitHub Actions runner. In every
# automated context (GitHub Actions, Streamlit Cloud) there is no .env file at
# all -- real environment variables/secrets are injected instead -- so this
# load is a harmless no-op there.
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = os.getenv("ACTOR_ID")

MAX_PRODUCTS = 50

TABLE_NAME = "flipkart_snapshots"


CATEGORY_URLS = {
    "smartphones":
        "https://www.flipkart.com/search?q=smartphones",

    "gaming_laptops":
        "https://www.flipkart.com/search?q=gaming+laptops",

    "tablets":
        "https://www.flipkart.com/search?q=tablets",

    "bluetooth_speakers":
        "https://www.flipkart.com/search?q=bluetooth+speakers",

    "computer_monitors":
        "https://www.flipkart.com/search?q=computer+monitors",

    "headphones":
        "https://www.flipkart.com/search?q=headphones",

    "smartwatches":
        "https://www.flipkart.com/search?q=smartwatches",

    "televisions":
        "https://www.flipkart.com/search?q=televisions",

    "cameras":
        "https://www.flipkart.com/search?q=cameras",

    "power_banks":
        "https://www.flipkart.com/search?q=power+banks"
}


SNAPSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "pipelines",
    "snapshots"
)

os.makedirs(
    SNAPSHOT_DIR,
    exist_ok=True
)


class SupabaseConfigError(RuntimeError):
    """Raised when Supabase credentials are missing or the client can't be built."""


@lru_cache(maxsize=1)
def get_supabase_client():
    """
    Lazy, cached Supabase client -- created on first actual use, not at import
    time, so a missing/bad credential fails loudly inside run_ingestion()'s
    per-category try/except (surfaced as "Failed for <category>: ...") rather
    than crashing the whole script before it can even scrape/save CSVs.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise SupabaseConfigError(
            "SUPABASE_URL / SUPABASE_KEY are not set. Set them in backend/.env "
            "for local dev, or as GitHub Actions repository secrets for the "
            "scheduled ingestion job."
        )

    from supabase import create_client
    return create_client(url, key)


def scrape_category(category_url):

    payload = {
        "proxyConfiguration": {
            "useApifyProxy": False
        },
        "results_wanted": MAX_PRODUCTS,
        "startUrl": category_url
    }

    response = requests.post(
        f"https://api.apify.com/v2/actors/{ACTOR_ID}/run-sync-get-dataset-items",
        params={
            "token": APIFY_TOKEN
        },
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return pd.DataFrame(data)


def save_snapshot(df, category, run_date):

    filepath = os.path.join(
        SNAPSHOT_DIR,
        f"{run_date}_{category}.csv"
    )

    df.to_csv(
        filepath,
        index=False
    )

    print(
        f"Saved local CSV backup: {filepath}"
    )


def _clean_value(value):
    """Convert a pandas cell into a JSON-serializable value: dict/list pass
    through as-is (they're already native Python objects here, straight from
    the Apify JSON response, not yet stringified by a CSV round-trip), NaN/NaT
    become None, and numpy scalars (int64/float64/bool_) become native Python
    types."""
    if isinstance(value, (dict, list)):
        return value
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _normalize_item_id(raw_item_id, fallback_flipkart_id):
    """Dedup/upsert key component. Flipkart's own id/item_id casing is
    inconsistent across categories (e.g. uppercase for cameras, lowercase for
    headphones) -- trim + lowercase whichever identifier is available, falling
    back to the CSV's "id" column (flipkart_id) if item_id itself is missing."""
    for candidate in (raw_item_id, fallback_flipkart_id):
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip().lower()
    return ""


def row_to_record(row: dict, category_slug: str, snapshot_date: str) -> dict | None:
    raw_item_id = row.get("item_id")
    flipkart_id = row.get("id")
    item_id = _normalize_item_id(raw_item_id, flipkart_id)

    if not item_id:
        # No usable identifier at all -- skip rather than write a row that can
        # never be deduped/upserted correctly on the next run.
        return None

    return {
        "item_id": item_id,
        "item_id_raw": _clean_value(raw_item_id),
        "flipkart_id": _clean_value(flipkart_id),
        "listing_id": _clean_value(row.get("listing_id")),
        "category_slug": category_slug,
        "title": _clean_value(row.get("title")),
        "brand": _clean_value(row.get("brand")),
        "category": _clean_value(row.get("category")),
        "price": _clean_value(row.get("price")),
        "price_text": _clean_value(row.get("price_text")),
        "original_price": _clean_value(row.get("original_price")),
        "original_price_text": _clean_value(row.get("original_price_text")),
        "discount_percent": _clean_value(row.get("discount_percent")),
        "discount_amount": _clean_value(row.get("discount_amount")),
        "discount_text": _clean_value(row.get("discount_text")),
        "rating": _clean_value(row.get("rating")),
        "rating_count": _clean_value(row.get("rating_count")),
        "review_count": _clean_value(row.get("review_count")),
        "rating_breakdown": _clean_value(row.get("rating_breakdown")),
        "specifications": _clean_value(row.get("specifications")),
        "key_specs": _clean_value(row.get("key_specs")),
        "warranty_summary": _clean_value(row.get("warranty_summary")),
        "availability_status": _clean_value(row.get("availability_status")),
        "is_available": _clean_value(row.get("is_available")),
        "buyability_intent": _clean_value(row.get("buyability_intent")),
        "is_flipkart_advantage": _clean_value(row.get("is_flipkart_advantage")),
        "swatch_available": _clean_value(row.get("swatch_available")),
        "currency": _clean_value(row.get("currency")),
        "analytics_category": _clean_value(row.get("analytics_category")),
        "analytics_sub_category": _clean_value(row.get("analytics_sub_category")),
        "market_place": _clean_value(row.get("market_place")),
        "image_url": _clean_value(row.get("image_url")),
        "url": _clean_value(row.get("url")),
        "fetched_at": _clean_value(row.get("fetched_at")) or datetime.now(timezone.utc).isoformat(),
        "snapshot_date": snapshot_date,
    }


def upsert_to_supabase(df, category_slug, snapshot_date):
    """Upsert this category's rows into flipkart_snapshots, keyed on
    (item_id, snapshot_date) so re-running the same day updates rather than
    duplicates. Returns the number of rows written."""
    records = [
        record
        for record in (
            row_to_record(row, category_slug, snapshot_date)
            for row in df.to_dict("records")
        )
        if record is not None
    ]

    skipped = len(df) - len(records)
    if skipped:
        print(f"  Skipping {skipped} row(s) with no usable item_id/id")

    # Apify sometimes returns the same product more than once in one batch
    # (e.g. the same item_id listed under different sellers/pages). Postgres's
    # upsert rejects a batch with duplicate conflict-target values outright
    # ("ON CONFLICT DO UPDATE command cannot affect row a second time"), which
    # was silently failing whole categories (seen for real: smartphones,
    # tablets, power_banks) -- so dedupe on item_id before sending, keeping
    # the first occurrence.
    deduped = {}
    for record in records:
        deduped.setdefault(record["item_id"], record)
    duplicates = len(records) - len(deduped)
    if duplicates:
        print(f"  Deduping {duplicates} duplicate item_id(s) within this batch")
    records = list(deduped.values())

    if not records:
        return 0

    client = get_supabase_client()
    client.table(TABLE_NAME).upsert(records, on_conflict="item_id,snapshot_date").execute()

    return len(records)


def run_ingestion():

    run_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    succeeded = []
    failed = []
    total_rows_written = 0

    for category, url in CATEGORY_URLS.items():

        print(
            f"\nFetching: {category}"
        )

        try:

            df = scrape_category(url)

            if df.empty:

                print(
                    f"No data returned for {category}"
                )

                continue

            print(
                f"Fetched {len(df)} products"
            )

            save_snapshot(
                df,
                category,
                run_date
            )

            rows_written = upsert_to_supabase(
                df,
                category,
                run_date
            )

            print(
                f"Upserted {rows_written} row(s) into Supabase ({TABLE_NAME})"
            )

            succeeded.append(category)
            total_rows_written += rows_written

        except Exception as e:

            print(
                f"Failed for {category}: {e}"
            )

            failed.append(category)

    print(
        f"\nIngestion completed. "
        f"{len(succeeded)}/{len(CATEGORY_URLS)} categories succeeded, "
        f"{total_rows_written} row(s) upserted to Supabase."
    )

    if failed:
        print(f"Failed categories: {', '.join(failed)}")

    return succeeded, failed, total_rows_written


if __name__ == "__main__":

    import sys

    _succeeded, _failed, _rows = run_ingestion()

    # Every category failing (0 rows written) is a real failure, not just a
    # partial one -- exit non-zero so a scheduled CI run shows red instead of
    # silently "succeeding" while writing no data.
    if _rows == 0:
        sys.exit(1)
