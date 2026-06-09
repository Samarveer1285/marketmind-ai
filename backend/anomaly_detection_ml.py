from analytics_function import *

from sklearn.ensemble import IsolationForest

import pandas as pd


def detect_ml_anomalies():

    merged = load_data()

    latest = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    data = latest[
        [
            "name",
            "price",
            "rating",
            "review_count"
        ]
    ].copy()

    features = data[
        [
            "price",
            "rating",
            "review_count"
        ]
    ]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    predictions = (
        model.fit_predict(
            features
        )
    )

    data["anomaly"] = predictions

    anomalies = data[
        data["anomaly"] == -1
    ]

    return anomalies