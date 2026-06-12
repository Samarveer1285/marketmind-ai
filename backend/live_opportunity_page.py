import pandas as pd

from market_monitor import get_latest_market_data


def generate_live_opportunities():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "name",
                "start_reviews",
                "end_reviews",
                "momentum_pct",
                "avg_rating",
                "risk_score",
                "opportunity_score"
            ]
        )

    opportunities = data.copy()
    opportunities["rating"] = (
        opportunities["rating"]
        .fillna(0)
    )

    opportunities["review_count"] = (
        opportunities["review_count"]
        .fillna(0)
    )

    opportunities["name"] = opportunities["product_name"]

    opportunities["review_count"] = (
        opportunities["review_count"]
        .fillna(0)
    )

    opportunities["start_reviews"] = (
        opportunities["review_count"] * 0.8
    ).astype(int)

    opportunities["end_reviews"] = (
        opportunities["review_count"]
    ).astype(int)

    opportunities["momentum_pct"] = (
        (
            opportunities["end_reviews"]
            - opportunities["start_reviews"]
        )
        / opportunities["start_reviews"]
        * 100
    ).round(1)

    opportunities["avg_rating"] = opportunities["rating"]

    opportunities["risk_score"] = (
        5 - opportunities["rating"]
    ).round(2)

    opportunities["opportunity_score"] = (
        opportunities["momentum_pct"] * 0.6
        + opportunities["avg_rating"] * 10
        - opportunities["risk_score"] * 5
    ).round(1)

    return opportunities[
        [
            "name",
            "start_reviews",
            "end_reviews",
            "momentum_pct",
            "avg_rating",
            "risk_score",
            "opportunity_score"
        ]
    ]