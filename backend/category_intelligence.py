from analytics_function import *
import pandas as pd


def get_category_growth():

    merged = load_data()

    latest_date = (
        merged["recorded_at"]
        .max()
    )

    previous_date = (
        merged["recorded_at"]
        .sort_values()
        .unique()[-2]
    )

    latest = merged[
        merged["recorded_at"] == latest_date
    ]

    previous = merged[
        merged["recorded_at"] == previous_date
    ]

    latest_category = (
        latest.groupby("category")
        ["review_count"]
        .sum()
        .reset_index()
    )

    previous_category = (
        previous.groupby("category")
        ["review_count"]
        .sum()
        .reset_index()
    )

    category_growth = (
        latest_category.merge(
            previous_category,
            on="category",
            suffixes=(
                "_latest",
                "_previous"
            )
        )
    )

    category_growth[
        "growth_pct"
    ] = (
        (
            category_growth[
                "review_count_latest"
            ]
            -
            category_growth[
                "review_count_previous"
            ]
        )
        /
        category_growth[
            "review_count_previous"
        ]
    ) * 100

    return (
        category_growth
        .sort_values(
            "growth_pct",
            ascending=False
        )
    )


def get_category_market_share():

    merged = load_data()

    latest = merged[
        merged["recorded_at"]
        ==
        merged["recorded_at"].max()
    ]

    category_sales = (
        latest.groupby("category")
        ["review_count"]
        .sum()
        .reset_index()
    )

    total = (
        category_sales[
            "review_count"
        ].sum()
    )

    category_sales[
        "market_share"
    ] = (
        category_sales[
            "review_count"
        ]
        / total
    ) * 100

    return (
        category_sales
        .sort_values(
            "market_share",
            ascending=False
        )
    )