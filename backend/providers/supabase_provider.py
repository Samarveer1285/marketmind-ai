"""
Supabase-backed implementation of DataProvider.

Reads from the `flipkart_snapshots` table (see db/schema.sql) — the single
source of truth for all product snapshot data, populated by the ingestion
pipeline.

The Supabase client is created lazily on first use, not at import time, so
importing this module never crashes the app. Connection/credential problems
surface as a clear ProviderError when a query is actually attempted, which
callers (Streamlit pages) can catch and show as a friendly message instead of
a raw traceback.
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from providers.provider_interface import DataProvider

# Resolve backend/.env relative to this file (backend/providers/supabase_provider.py
# -> backend/.env), not the process's current working directory — a bare
# load_dotenv() only finds it if the app happens to be launched from backend/.
# In deployment there is no .env file at all; Streamlit Cloud injects secrets as
# real environment variables instead, so this is a harmless no-op there and
# os.getenv() below picks those up directly.
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

TABLE_NAME = "flipkart_snapshots"
PAGE_SIZE = 1000


class ProviderError(RuntimeError):
    """Raised when the Supabase provider can't connect to or query Supabase."""


class SupabaseProvider(DataProvider):

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ProviderError(
                "SUPABASE_URL / SUPABASE_KEY are not set. Set them in "
                "backend/.env for local dev, or in Streamlit Cloud's Secrets "
                "panel for the deployed app."
            )

        try:
            from supabase import create_client
            self._client = create_client(url, key)
        except Exception as exc:
            raise ProviderError(f"Could not connect to Supabase: {exc}") from exc

        return self._client

    @staticmethod
    def _fetch_all(build_query) -> pd.DataFrame:
        """
        Page through a PostgREST query in chunks of PAGE_SIZE rows.

        `build_query` is a zero-arg callable returning a *fresh* query builder
        each time it's called, since a builder shouldn't be re-executed after
        `.execute()` has already been called on it.
        """
        rows = []
        start = 0

        while True:
            page = build_query().range(start, start + PAGE_SIZE - 1).execute()
            data = page.data or []
            rows.extend(data)

            if len(data) < PAGE_SIZE:
                break
            start += PAGE_SIZE

        return pd.DataFrame(rows)

    def get_latest_snapshot(self) -> pd.DataFrame:
        """
        Latest snapshot, grouped by our own category_slug (the CATEGORY_URLS key
        each product was scraped under, e.g. "headphones") — not the broader
        analytics_category, which merges related slugs together (e.g. headphones
        and bluetooth_speakers both roll up to "PersonalAudio").
        """
        client = self._get_client()

        try:
            date_rows = (
                client.table(TABLE_NAME)
                .select("category_slug, snapshot_date")
                .execute()
                .data
            )
        except Exception as exc:
            raise ProviderError(f"Could not query {TABLE_NAME}: {exc}") from exc

        if not date_rows:
            return pd.DataFrame()

        latest_by_category = (
            pd.DataFrame(date_rows)
            .groupby("category_slug")["snapshot_date"]
            .max()
            .to_dict()
        )

        frames = []
        for category_slug, snapshot_date in latest_by_category.items():
            try:
                resp = (
                    client.table(TABLE_NAME)
                    .select("*")
                    .eq("category_slug", category_slug)
                    .eq("snapshot_date", snapshot_date)
                    .execute()
                )
            except Exception as exc:
                raise ProviderError(f"Could not query {TABLE_NAME}: {exc}") from exc
            frames.append(pd.DataFrame(resp.data or []))

        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def get_historical_snapshots(self, days: int | None = None) -> pd.DataFrame:
        client = self._get_client()
        cutoff = None
        if days is not None:
            cutoff = (datetime.now(timezone.utc).date() - timedelta(days=days)).isoformat()

        def build_query():
            query = client.table(TABLE_NAME).select("*").order("snapshot_id")
            if cutoff is not None:
                query = query.gte("snapshot_date", cutoff)
            return query

        try:
            return self._fetch_all(build_query)
        except Exception as exc:
            raise ProviderError(f"Could not query {TABLE_NAME}: {exc}") from exc
