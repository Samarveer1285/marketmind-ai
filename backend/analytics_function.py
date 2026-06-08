from database import supabase
import pandas as pd
import numpy as np


def load_data():

    products = supabase.table(
        "products"
    ).select("*").execute()

    price_history = supabase.table(
        "price_history"
    ).select("*").execute()

    products_df = pd.DataFrame(
        products.data
    )

    prices_df = pd.DataFrame(
        price_history.data
    )

    merged = prices_df.merge(
        products_df,
        left_on="product_id",
        right_on="id"
    )

    return merged
def get_brand_health():

    merged = load_data()

    brand_health = (
        merged
        .groupby("brand")
        .agg({
            "rating":"mean",
            "review_count":"mean",
            "price":"mean"
        })
        .reset_index()
    )

    brand_health[
        "brand_health_score"
    ] = (
        brand_health["rating"] * 20
        +
        np.log1p(
            brand_health["review_count"]
        ) * 5
    )

    return (
        brand_health
        .sort_values(
            by="brand_health_score",
            ascending=False
        )
    )
def get_market_leaderboard():

    merged = load_data()

    leaderboard = (
        merged
        .groupby("name")
        .agg({
            "rating":"mean",
            "review_count":"mean"
        })
        .reset_index()
    )

    leaderboard["market_score"] = (
        leaderboard["rating"] * 10
        +
        np.log1p(
            leaderboard["review_count"]
        ) * 5
    )

    return (
        leaderboard
        .sort_values(
            by="market_score",
            ascending=False
        )
    )
def get_hidden_gems():

    merged = load_data()

    avg_reviews = (
        merged["review_count"]
        .mean()
    )

    hidden_gems = merged[
        (
            merged["rating"] >= 4.5
        )
        &
        (
            merged["review_count"]
            < avg_reviews
        )
    ]

    return hidden_gems[
        [
            "name",
            "rating",
            "review_count"
        ]
    ]
def get_price_volatility():

    merged = load_data()

    volatility = (
        merged
        .groupby("name")["price"]
        .std()
        .reset_index()
    )

    volatility.columns = [
        "name",
        "price_volatility"
    ]

    return volatility.sort_values(
        by="price_volatility",
        ascending=False
    )
def get_revenue_opportunity():

    merged = load_data()

    latest_products = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    latest_products["opportunity_score"] = (
        latest_products["rating"] * 20
        -
        np.log1p(
            latest_products["review_count"]
        ) * 5
    )

    return (
        latest_products[
            [
                "name",
                "price",
                "rating",
                "review_count",
                "opportunity_score"
            ]
        ]
        .sort_values(
            by="opportunity_score",
            ascending=False
        )
    )
def get_opportunity_matrix():

    merged = load_data()

    avg_rating = merged["rating"].mean()
    avg_reviews = merged["review_count"].mean()

    matrix = (
        merged
        .groupby("name")
        .agg({
            "rating":"mean",
            "review_count":"mean"
        })
        .reset_index()
    )

    def classify(row):

        if (
            row["rating"] >= avg_rating
            and
            row["review_count"] >= avg_reviews
        ):
            return "Star"

        elif (
            row["rating"] >= avg_rating
            and
            row["review_count"] < avg_reviews
        ):
            return "Hidden Gem"

        elif (
            row["rating"] < avg_rating
            and
            row["review_count"] >= avg_reviews
        ):
            return "Needs Attention"

        else:
            return "Poor Performer"

    matrix["category"] = matrix.apply(
        classify,
        axis=1
    )

    return matrix
def get_customer_trust():

    merged = load_data()

    merged["trust_score"] = (
        merged["rating"]
        *
        np.log1p(
            merged["review_count"]
        )
    )

    return (
        merged[
            ["name", "trust_score"]
        ]
        .sort_values(
            by="trust_score",
            ascending=False
        )
    )
def get_overpriced_products():

    merged = load_data()

    avg_price = merged["price"].mean()

    return merged[
        merged["price"] >
        avg_price * 1.15
    ][
        [
            "name",
            "price"
        ]
    ]
def get_undervalued_products():

    merged = load_data()

    latest_prices = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .tail(1)
    )

    latest_prices["value_score"] = (
        latest_prices["rating"]
        /
        (
            latest_prices["price"]
            / 10000
        )
    )

    return (
        latest_prices[
            [
                "name",
                "price",
                "rating",
                "value_score"
            ]
        ]
        .sort_values(
            by="value_score",
            ascending=False
        )
    )
def get_biggest_price_drops():

    merged = load_data()

    price_trend = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .agg(
            first_price=("price", "first"),
            last_price=("price", "last")
        )
        .reset_index()
    )

    price_trend["price_change_pct"] = (
        (
            price_trend["last_price"]
            -
            price_trend["first_price"]
        )
        /
        price_trend["first_price"]
    ) * 100

    return price_trend.sort_values(
        by="price_change_pct"
    )
def get_demand_momentum():

    merged = load_data()

    momentum = (
        merged
        .sort_values("recorded_at")
        .groupby("name")
        .agg(
            start_reviews=("review_count", "first"),
            end_reviews=("review_count", "last")
        )
        .reset_index()
    )

    momentum["momentum_pct"] = (
        (
            momentum["end_reviews"]
            -
            momentum["start_reviews"]
        )
        /
        momentum["start_reviews"]
    ) * 100

    return momentum.sort_values(
        by="momentum_pct",
        ascending=False
    )
def get_review_growth():

    return get_demand_momentum()
def get_risk_products():

    merged = load_data()

    risk_products = (
        merged
        .groupby("name")
        .agg(
            avg_rating=("rating", "mean")
        )
        .reset_index()
    )

    risk_products["risk_score"] = (
        (
            5
            -
            risk_products["avg_rating"]
        )
        * 10
    )

    return risk_products.sort_values(
        by="risk_score",
        ascending=False
    )
def get_brand_growth():

    merged = load_data()

    brand_growth = (
        merged
        .sort_values("recorded_at")
        .groupby("brand")
        .agg(
            start_reviews=("review_count", "first"),
            end_reviews=("review_count", "last"),
            avg_rating=("rating", "mean")
        )
        .reset_index()
    )

    brand_growth["growth_pct"] = (
        (
            brand_growth["end_reviews"]
            -
            brand_growth["start_reviews"]
        )
        /
        brand_growth["start_reviews"]
    ) * 100

    brand_growth["brand_growth_score"] = (
        brand_growth["growth_pct"] * 0.7
        +
        brand_growth["avg_rating"] * 10 * 0.3
    )

    return brand_growth.sort_values(
        by="brand_growth_score",
        ascending=False
    )

