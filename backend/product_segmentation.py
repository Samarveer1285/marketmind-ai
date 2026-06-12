import pandas as pd

from market_monitor import get_latest_market_data


def get_product_segments():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "name",
                "price",
                "rating",
                "review_count",
                "momentum_pct",
                "segment"
            ]
        )

    segments = data.copy()

    segments["name"] = segments["product_name"]
    segments["price"] = pd.to_numeric(
        segments["price"],
        errors="coerce"
    )

    segments["rating"] = pd.to_numeric(
        segments["rating"],
        errors="coerce"
    )

    segments["review_count"] = pd.to_numeric(
        segments["review_count"],
        errors="coerce"
    )

    segments = segments.dropna(
        subset=[
            "price",
            "rating",
            "review_count"
        ]
    )

    # Simulated momentum using current reviews
    segments["momentum_pct"] = (
        segments["review_count"] * 0.20
    ).round(1)

    median_reviews = (
        segments["review_count"]
        .median()
    )

    segments["segment"] = "Mass Market"

    segments.loc[
        (
            (segments["rating"] >= 4.5)
            &
            (segments["review_count"] >= median_reviews)
        ),
        "segment"
    ] = "Premium Leaders"

    segments.loc[
        (
            (segments["rating"] >= 4.5)
            &
            (segments["review_count"] < median_reviews)
        ),
        "segment"
    ] = "Hidden Gems"

    segments.loc[
        (
            (segments["rating"] < 4)
            &
            (segments["review_count"] >= median_reviews)
        ),
        "segment"
    ] = "Risky Underperformers"

    segments.loc[
        (
            (segments["rating"] >= 4)
            &
            (segments["rating"] < 4.5)
            &
            (segments["review_count"] >= median_reviews)
        ),
        "segment"
    ] = "Growth Champions"

    return segments[
        [
            "name",
            "price",
            "rating",
            "review_count",
            "momentum_pct",
            "segment"
        ]
    ]