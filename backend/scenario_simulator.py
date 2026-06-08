from analytics_function import *
import pandas as pd
import numpy as np


def simulate_price_change(
    product_name,
    price_change_pct
):

    merged = load_data()

    latest = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    product = latest[
        latest["name"] == product_name
    ]

    if len(product) == 0:

        return None

    current_price = (
        product["price"]
        .iloc[0]
    )

    rating = (
        product["rating"]
        .iloc[0]
    )

    reviews = (
        product["review_count"]
        .iloc[0]
    )

    new_price = (
        current_price
        *
        (
            1
            +
            price_change_pct / 100
        )
    )

    demand_change = (
        -1.5
        *
        price_change_pct
    )

    projected_reviews = (
        reviews
        *
        (
            1
            +
            demand_change / 100
        )
    )

    return pd.DataFrame({

        "product":[product_name],

        "current_price":[
            round(current_price,2)
        ],

        "new_price":[
            round(new_price,2)
        ],

        "current_reviews":[
            reviews
        ],

        "projected_reviews":[
            round(
                projected_reviews,
                0
            )
        ],

        "demand_change_pct":[
            round(
                demand_change,
                2
            )
        ]
    })

def simulate_rating_improvement(
    product_name,
    new_rating
):

    merged = load_data()

    latest = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    product = latest[
        latest["name"] == product_name
    ]

    if len(product) == 0:

        return None

    current_rating = (
        product["rating"]
        .iloc[0]
    )

    reviews = (
        product["review_count"]
        .iloc[0]
    )

    current_trust_score = (
        current_rating
        *
        reviews
    )

    projected_trust_score = (
        new_rating
        *
        reviews
    )

    trust_change_pct = (
        (
            projected_trust_score
            -
            current_trust_score
        )
        /
        current_trust_score
    ) * 100

    current_opportunity = (
        current_rating * 20
        -
        np.log1p(reviews) * 5
    )

    projected_opportunity = (
        new_rating * 20
        -
        np.log1p(reviews) * 5
    )

    return pd.DataFrame({

        "product":[
            product_name
        ],

        "current_rating":[
            round(
                current_rating,
                2
            )
        ],

        "projected_rating":[
            round(
                new_rating,
                2
            )
        ],

        "current_trust_score":[
            round(
                current_trust_score,
                2
            )
        ],

        "projected_trust_score":[
            round(
                projected_trust_score,
                2
            )
        ],

        "trust_change_pct":[
            round(
                trust_change_pct,
                2
            )
        ],

        "current_opportunity":[
            round(
                current_opportunity,
                2
            )
        ],

        "projected_opportunity":[
            round(
                projected_opportunity,
                2
            )
        ]
    })
def simulate_review_growth(
    product_name,
    growth_pct
):

    merged = load_data()

    latest = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    product = latest[
        latest["name"] == product_name
    ]

    if len(product) == 0:

        return None

    rating = (
        product["rating"]
        .iloc[0]
    )

    reviews = (
        product["review_count"]
        .iloc[0]
    )

    current_market_score = (
        rating * 10
        +
        np.log1p(reviews) * 5
    )

    projected_reviews = (
        reviews
        *
        (
            1
            +
            growth_pct / 100
        )
    )

    projected_market_score = (
        rating * 10
        +
        np.log1p(
            projected_reviews
        ) * 5
    )

    current_trust_score = (
        rating
        *
        np.log1p(reviews)
    )

    projected_trust_score = (
        rating
        *
        np.log1p(
            projected_reviews
        )
    )

    return pd.DataFrame({

        "product":[
            product_name
        ],

        "current_reviews":[
            reviews
        ],

        "projected_reviews":[
            round(
                projected_reviews,
                0
            )
        ],

        "current_market_score":[
            round(
                current_market_score,
                2
            )
        ],

        "projected_market_score":[
            round(
                projected_market_score,
                2
            )
        ],

        "current_trust_score":[
            round(
                current_trust_score,
                2
            )
        ],

        "projected_trust_score":[
            round(
                projected_trust_score,
                2
            )
        ]
    })