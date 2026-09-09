import pandas as pd
import numpy as np

from providers import get_provider


def load_data():
    """
    Full snapshot history, renamed to the column names every function below
    already expects (name/brand/price/rating/review_count/recorded_at).
    Previously this queried Supabase's old "products"/"price_history" tables
    directly -- which only ever held synthetic/random demo data, disconnected
    from the real Flipkart scrapes -- via a module-level `from database import
    supabase` that crashed on import if credentials were missing. Now sourced
    from the shared provider (real data), with no import-time crash risk.
    """
    merged = get_provider().get_historical_snapshots()

    if merged.empty:
        # No snapshots yet (e.g. before the first ingestion run has landed
        # any rows). Every function below assumes these columns exist even
        # on zero rows -- a bare pd.DataFrame() has none, which turns into a
        # raw KeyError traceback on the very first .groupby()/.sort_values()
        # a caller does. Return an empty frame shaped like the real one.
        return pd.DataFrame(columns=[
            "name", "brand", "category", "price", "rating",
            "review_count", "recorded_at",
        ])

    merged = merged.copy()
    merged["name"] = merged["title"]
    merged["recorded_at"] = pd.to_datetime(merged["snapshot_date"])

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

