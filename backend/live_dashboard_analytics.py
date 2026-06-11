from market_monitor import get_latest_market_data
import pandas as pd


def get_live_brand_health():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "brand",
                "brand_health_score"
            ]
        )

    brand_health = (
        data.groupby("keyword")
        .agg(
            avg_rating=("rating", "mean"),
            total_reviews=("review_count", "sum")
        )
        .reset_index()
    )

    brand_health["brand_health_score"] = (
        brand_health["avg_rating"] * 20
        +
        brand_health["total_reviews"] / 1000
    )

    brand_health = (
        brand_health
        .rename(
            columns={
                "keyword": "brand"
            }
        )
        .sort_values(
            "brand_health_score",
            ascending=False
        )
    )

    return brand_health[
        [
            "brand",
            "brand_health_score"
        ]
    ]


def get_live_market_leaderboard():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "name",
                "market_score"
            ]
        )

    leaderboard = data.copy()

    leaderboard["market_score"] = (
        leaderboard["rating"] * 100
        +
        leaderboard["review_count"] / 100
        -
        leaderboard["price"] / 50
    )

    leaderboard = leaderboard.sort_values(
        "market_score",
        ascending=False
    )

    return leaderboard.rename(
        columns={
            "product_name": "name"
        }
    )


def get_live_hidden_gems():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    gems = data[
        (
            data["rating"] >= 4.2
        )
        &
        (
            data["review_count"]
            <
            data["review_count"].median()
        )
    ]

    return gems.rename(
        columns={
            "product_name": "name"
        }
    )


def get_live_opportunity_matrix():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    matrix = data.copy()

    matrix["opportunity_score"] = (
        matrix["rating"] * 100
        +
        matrix["review_count"] / 100
        -
        matrix["price"] / 50
    )

    return matrix.rename(
        columns={
            "keyword": "category",
            "product_name": "name"
        }
    )
def get_live_demand_momentum():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "name",
                "momentum_pct"
            ]
        )

    momentum = data.copy()

    momentum["momentum_pct"] = (
        momentum["review_count"]
        /
        momentum["review_count"].sum()
        *
        100
    )

    momentum = momentum.sort_values(
        "momentum_pct",
        ascending=False
    )

    return momentum.rename(
        columns={
            "product_name": "name"
        }
    )
