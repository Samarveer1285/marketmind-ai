import pandas as pd

from providers import get_provider


def build_historical_timeseries():
    """
    Full snapshot history, shaped for the forecasting functions below
    (product_name, snapshot_date as a real date). Previously this read
    pipelines/snapshots/*.csv directly and referenced "timestamp" and
    "product_name" columns that don't actually exist in the real CSVs (only
    "fetched_at" and "title" do) — meaning this was silently broken against
    real data. Now sourced from the shared provider and renamed correctly.
    """
    history = get_provider().get_historical_snapshots()

    if history.empty:
        return history

    history = history.copy()

    if "title" in history.columns:
        history["product_name"] = history["title"]

    history["snapshot_date"] = pd.to_datetime(
        history["snapshot_date"]
    ).dt.date

    return history.sort_values("snapshot_date")

def get_product_history(product_name):

    history = build_historical_timeseries()

    if history.empty:
        return pd.DataFrame()

    product_history = history[
        history["product_name"] == product_name
    ].copy()

    if product_history.empty:
        return pd.DataFrame()

    product_history = (
        product_history
        .groupby("snapshot_date")
        .agg(
            review_count=("review_count", "mean"),
            price=("price", "mean"),
            rating=("rating", "mean")
        )
        .reset_index()
        .sort_values("snapshot_date")
    )

    return product_history
def generate_live_forecast(product_name):

    history = get_product_history(product_name)

    if history.empty:

        return {
            "status": "No Data",
            "current_value": None,
            "forecast_value": None,
            "confidence": "Low",
            "trend": "Unknown"
        }

    current_reviews = history.iloc[-1]["review_count"]

    if pd.isna(current_reviews):
        # review_count is null for ~21-23% of scraped rows -- if this
        # product's latest snapshot is one of them, there's nothing to
        # forecast from.
        return {
            "status": "No Data",
            "current_value": None,
            "forecast_value": None,
            "confidence": "Low",
            "trend": "Unknown"
        }

    n_days = len(history)

    # Only 1 day available
    if n_days == 1:

        return {
            "status": "Insufficient History",
            "current_value": int(current_reviews),
            "forecast_value": int(current_reviews),
            "confidence": "Low",
            "trend": "Stable"
        }

    # Simple trend forecast
    previous_reviews = history.iloc[-2]["review_count"]

    if pd.isna(previous_reviews):
        # Same idea, one snapshot back -- fall back to treating today's
        # value as the whole (short) history rather than crashing.
        return {
            "status": "Insufficient History",
            "current_value": int(current_reviews),
            "forecast_value": int(current_reviews),
            "confidence": "Low",
            "trend": "Stable"
        }

    growth = current_reviews - previous_reviews

    forecast = current_reviews + growth

    if growth > 0:
        trend = "Increasing"
    elif growth < 0:
        trend = "Declining"
    else:
        trend = "Stable"

    confidence = (
        "Medium"
        if n_days < 7
        else "High"
    )

    return {
        "status": "Forecast Available",
        "current_value": int(current_reviews),
        "forecast_value": int(forecast),
        "confidence": confidence,
        "trend": trend
    }
def get_live_forecast_dataset():

    history = build_historical_timeseries()

    if history.empty:
        return pd.DataFrame()

    products = history["product_name"].unique()

    forecasts = []

    for product in products:

        result = generate_live_forecast(product)

        if result["current_value"] is None:
            continue

        forecasts.append({
            "product": product,
            "current_reviews": result["current_value"],
            "forecast_reviews": result["forecast_value"],
            "trend": result["trend"],
            "confidence": result["confidence"]
        })

    return pd.DataFrame(forecasts)