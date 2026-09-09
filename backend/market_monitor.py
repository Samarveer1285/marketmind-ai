import pandas as pd

from providers import get_provider


def get_latest_market_data():
    """
    Despite the name, this has always returned the FULL available history
    (every snapshot_date, every category) concatenated together, not just the
    latest snapshot — kept as-is here since 11 downstream modules
    (live_dashboard_analytics, live_forecasting, product_segmentation, etc.)
    rely on that full-history shape for trend/momentum calculations. Data now
    comes from the shared Supabase-backed provider instead of a raw CSV glob.
    """
    data = get_provider().get_historical_snapshots()

    if data.empty:
        return data

    if "title" in data.columns:
        data["product_name"] = data["title"]

    if "analytics_category" in data.columns:
        data["keyword"] = data["analytics_category"]

    elif "category" in data.columns:
        data["keyword"] = data["category"]

    return data


def get_market_summary():

    data = get_latest_market_data()

    if data.empty:

        return {
            "products": 0,
            "categories": 0,
            "avg_rating": 0,
            "avg_price": 0
        }

    return {

        "products":
            len(data),

        "categories":
            data["keyword"].nunique(),

        "avg_rating":
            round(
                data["rating"].mean(),
                2
            ),

        "avg_price":
            round(
                data["price"].mean(),
                0
            )
    }
