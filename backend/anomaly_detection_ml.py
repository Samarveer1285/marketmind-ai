import pandas as pd

from sklearn.ensemble import IsolationForest

from market_monitor import get_latest_market_data


def detect_ml_anomalies():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "name",
                "price",
                "rating",
                "review_count",
                "anomaly"
            ]
        )

    df = data.copy()

    df["name"] = df["product_name"]

    features = df[
        [
            "price",
            "rating",
            "review_count"
        ]
    ].copy()

    # Handle missing values
    features["price"] = (
        features["price"]
        .fillna(
            features["price"].median()
        )
    )

    features["rating"] = (
        features["rating"]
        .fillna(3)
    )

    features["review_count"] = (
        features["review_count"]
        .fillna(0)
    )

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(
        features
    )

    return df[
        [
            "name",
            "price",
            "rating",
            "review_count",
            "anomaly"
        ]
    ]