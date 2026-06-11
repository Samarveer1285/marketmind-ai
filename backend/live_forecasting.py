import os
import pandas as pd
from pathlib import Path

SNAPSHOT_DIR = Path("pipelines/snapshots")


def build_historical_timeseries():

    all_records = []

    if not SNAPSHOT_DIR.exists():
        return pd.DataFrame()

    snapshot_files = list(
        SNAPSHOT_DIR.glob("*.csv")
    )

    for file in snapshot_files:

        try:

            data = pd.read_csv(file)

            if data.empty:
                continue

            data["snapshot_date"] = (
                pd.to_datetime(
                    data["timestamp"]
                ).dt.date
            )

            all_records.append(data)

        except Exception:
            continue

    if len(all_records) == 0:
        return pd.DataFrame()

    history = pd.concat(
        all_records,
        ignore_index=True
    )

    history = history.sort_values(
        "snapshot_date"
    )

    return history

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