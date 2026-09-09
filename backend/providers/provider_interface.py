from abc import ABC, abstractmethod

import pandas as pd


class DataProvider(ABC):

    """
    Base interface for all market data providers.

    Every provider must return a DataFrame shaped like the `flipkart_snapshots`
    table (see db/schema.sql) — item_id, title, brand, category, price,
    original_price, discount_percent, rating, rating_count, review_count,
    specifications, key_specs, analytics_category, analytics_sub_category,
    market_place, image_url, url, fetched_at, snapshot_date, etc. — so that
    the rest of MarketMind (pages, analytics modules, the AI Copilot) can read
    from any implementation without caring where the data actually comes from.
    """

    @abstractmethod
    def get_latest_snapshot(self) -> pd.DataFrame:
        """
        Return the most recent snapshot for every product across every
        category. "Most recent" is per-category (each category's own latest
        snapshot_date), since categories can be refreshed on different runs.
        """
        raise NotImplementedError

    @abstractmethod
    def get_historical_snapshots(self, days: int | None = None) -> pd.DataFrame:
        """
        Return snapshot rows across every category and snapshot_date, for
        trend/momentum analysis (price history, review growth, forecasting).

        Parameters
        ----------
        days : int | None
            If given, only return rows whose snapshot_date is within the last
            `days` days. If None, return the full available history.
        """
        raise NotImplementedError
