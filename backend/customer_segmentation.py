from analytics_function import *

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

import pandas as pd


def get_customer_segments():

    merged = load_data()

    latest = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    customer_data = latest[
        [
            "name",
            "price",
            "rating",
            "review_count"
        ]
    ].copy()

    customer_data.rename(
        columns={
            "name": "customer"
        },
        inplace=True
    )

    features = customer_data[
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

    customer_data[
        "segment"
    ] = model.fit_predict(
        scaled
    )

    segment_names = {
        0: "High Value",
        1: "Loyal",
        2: "Growth",
        3: "Low Engagement"
    }

    customer_data[
        "segment_name"
    ] = customer_data[
        "segment"
    ].map(
        segment_names
    )

    return customer_data