import pandas as pd

from market_monitor import get_latest_market_data


def get_live_brand_benchmark():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    benchmark = (
        data.groupby("brand")
        .agg(
            avg_rating=("rating", "mean"),
            total_reviews=("review_count", "sum"),
            avg_price=("price", "mean")
        )
        .reset_index()
    )

    benchmark["benchmark_score"] = (
        benchmark["avg_rating"] * 20
        + benchmark["total_reviews"] / 1000
    ).round(1)

    return benchmark.sort_values(
        "benchmark_score",
        ascending=False
    )


def get_live_category_leaders():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    leaders = (
        data.sort_values(
            "review_count",
            ascending=False
        )
        .groupby("category")
        .head(1)
    )

    return leaders[
        [
            "category",
            "brand",
            "review_count"
        ]
    ].reset_index(drop=True)