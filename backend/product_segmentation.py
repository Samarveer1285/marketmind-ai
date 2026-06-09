from analytics_function import *

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import pandas as pd


def get_product_segments():

    merged = load_data()

    latest = merged[
        merged["recorded_at"]
        ==
        merged["recorded_at"].max()
    ]

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

    scaler = StandardScaler()

    scaled = scaler.fit_transform(
        features
    )

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    data["segment"] = (
        model.fit_predict(
            scaled
        )
    )

    return data