import pandas as pd

from load_products import get_latest_market_data


def get_live_brand_benchmark():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    benchmark = (
        data.groupby("keyword")
        .agg(
            avg_rating=("rating", "mean"),
            total_reviews=("review_count", "sum"),
            avg_price=("price", "mean")
        )
        .reset_index()
    )

    benchmark.rename(
        columns={
            "keyword": "brand"
        },
        inplace=True
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
        .groupby("keyword")
        .head(1)
    )

    leaders = leaders.rename(
        columns={
            "keyword": "category",
            "product_name": "brand"
        }
    )

    return leaders[
        [
            "category",
            "brand",
            "review_count"
        ]
    ]