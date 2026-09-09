"""
Provider factory — selects the active DataProvider implementation.

Set DATA_PROVIDER=mock in the environment to use synthetic local data with
no Supabase credentials required. Anything else (including unset) defaults
to the real Supabase-backed provider.
"""

import os
from functools import lru_cache

from providers.provider_interface import DataProvider


@lru_cache(maxsize=1)
def get_provider() -> DataProvider:
    """Return the shared DataProvider instance selected by DATA_PROVIDER."""
    backend = os.getenv("DATA_PROVIDER", "supabase").strip().lower()

    if backend == "mock":
        from providers.mock_provider import MockProvider
        return MockProvider()

    from providers.supabase_provider import SupabaseProvider
    return SupabaseProvider()
