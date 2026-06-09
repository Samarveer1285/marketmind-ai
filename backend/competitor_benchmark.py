from analytics_function import *

import pandas as pd


def get_brand_benchmark():

    merged = load_data()

    latest = merged[
        merged["recorded_at"]
        ==
        merged["recorded_at"].max()
    ]

    benchmark = (

        latest.groupby(
            ["brand"]
        )

        .agg({

            "rating": "mean",

            "review_count": "sum",

            "price": "mean"

        })

        .reset_index()

    )

    benchmark.rename(

        columns={

            "rating":
                "avg_rating",

            "review_count":
                "total_reviews",

            "price":
                "avg_price"

        },

        inplace=True

    )

    benchmark["benchmark_score"] = (

        benchmark["avg_rating"] * 20

        +

        benchmark["total_reviews"] / 100

    )

    return (

        benchmark.sort_values(
            "benchmark_score",
            ascending=False
        )

    )


def get_category_leaders():

    merged = load_data()

    latest = merged[
        merged["recorded_at"]
        ==
        merged["recorded_at"].max()
    ]

    category_brand = (

        latest.groupby(
            ["category", "brand"]
        )["review_count"]

        .sum()

        .reset_index()

    )

    leaders = (

        category_brand
        .sort_values(
            "review_count",
            ascending=False
        )

        .groupby("category")
        .head(1)

    )

    return leaders