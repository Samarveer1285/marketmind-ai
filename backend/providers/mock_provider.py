"""
In-memory mock implementation of DataProvider — no credentials required.

Used for local development/demo via DATA_PROVIDER=mock. Generates synthetic
rows shaped like real flipkart_snapshots rows (same columns, same category
slugs as the real Apify pipeline) so downstream analytics code behaves
identically regardless of which provider is active.
"""

import random
from datetime import datetime, timedelta, timezone

import pandas as pd

from providers.provider_interface import DataProvider

# Same 10 category slugs the real Apify pipeline scrapes (backend/daily_ingestion.py).
ANALYTICS_CATEGORY_BY_SLUG = {
    "bluetooth_speakers": "PersonalAudio",
    "cameras": "Camera",
    "computer_monitors": "ComputerMonitor",
    "gaming_laptops": "Laptop",
    "headphones": "PersonalAudio",
    "power_banks": "PowerBank",
    "smartphones": "Smartphone",
    "smartwatches": "Smartwatch",
    "tablets": "Tablet",
    "televisions": "Television",
}

BRANDS = ["Samsung", "Sony", "boAt", "Noise", "OnePlus", "Realme", "JBL", "Apple", "Mi", "LG"]

PRODUCTS_PER_CATEGORY = 8
# Two synthetic snapshot dates (today, and a few days back) so momentum/trend
# code has something to compute a delta against.
HISTORY_OFFSETS_DAYS = [0, 3]


class MockProvider(DataProvider):
    """
    Identity fields (item_id, brand, title) are assigned once per item_id and
    reused on every call/date; only time-varying fields (price, rating,
    review_count, ...) are re-rolled per snapshot_date. This mirrors how a
    real database behaves (the same product keeps the same name across
    snapshots) so that analytics code joining/grouping across two separate
    provider calls by name/item_id (e.g. recommendation_engine.py matching
    get_demand_momentum() against forecast_price()) sees consistent products,
    not a fresh random catalog on every call.
    """

    def __init__(self):
        self._brand_by_item: dict[str, str] = {}
        self._snapshot_cache: dict[str, list[dict]] = {}

    def _brand_for(self, item_id: str) -> str:
        if item_id not in self._brand_by_item:
            self._brand_by_item[item_id] = random.choice(BRANDS)
        return self._brand_by_item[item_id]

    def _generate(self, snapshot_date) -> list[dict]:
        cache_key = snapshot_date.isoformat()
        if cache_key in self._snapshot_cache:
            return self._snapshot_cache[cache_key]

        fetched_at = datetime(
            snapshot_date.year, snapshot_date.month, snapshot_date.day, tzinfo=timezone.utc
        )
        rows = []

        for slug, analytics_category in ANALYTICS_CATEGORY_BY_SLUG.items():
            for i in range(1, PRODUCTS_PER_CATEGORY + 1):
                item_id = f"mock-{slug}-{i}"
                brand = self._brand_for(item_id)
                price = random.randint(500, 80000)

                rows.append({
                    "item_id": item_id,
                    "item_id_raw": item_id.upper(),
                    "flipkart_id": f"MOCKPID{i}",
                    "listing_id": f"MOCKLST{i}",
                    "category_slug": slug,
                    "title": f"{brand} {slug.replace('_', ' ').title()} {i}",
                    "brand": brand,
                    "category": slug,
                    "price": price,
                    "price_text": f"₹{price}",
                    "original_price": round(price * random.uniform(1.0, 1.3)),
                    "discount_percent": random.randint(0, 30),
                    "rating": round(random.uniform(3.0, 4.9), 1),
                    "rating_count": random.randint(10, 5000),
                    "review_count": random.randint(5, 3000),
                    "rating_breakdown": {},
                    "specifications": {},
                    "key_specs": [],
                    "availability_status": "IN_STOCK",
                    "is_available": True,
                    "currency": "INR",
                    "analytics_category": analytics_category,
                    "analytics_sub_category": analytics_category,
                    "market_place": "FLIPKART",
                    "image_url": "",
                    "url": "",
                    "fetched_at": fetched_at.isoformat(),
                    "snapshot_date": snapshot_date.isoformat(),
                })

        self._snapshot_cache[cache_key] = rows
        return rows

    def get_latest_snapshot(self) -> pd.DataFrame:
        today = datetime.now(timezone.utc).date()
        return pd.DataFrame(self._generate(today))

    def get_historical_snapshots(self, days: int | None = None) -> pd.DataFrame:
        today = datetime.now(timezone.utc).date()
        offsets = [d for d in HISTORY_OFFSETS_DAYS if days is None or d <= days]
        if not offsets:
            offsets = [0]

        rows = []
        for offset in offsets:
            rows.extend(self._generate(today - timedelta(days=offset)))

        return pd.DataFrame(rows)

    def get_last_refreshed(self):
        return datetime.now(timezone.utc)
