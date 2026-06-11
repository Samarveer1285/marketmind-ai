from market_monitor import get_latest_market_data


def generate_live_opportunities():

    data = get_latest_market_data()

    if data.empty:
        return []

    opportunities = data.copy()

    opportunities["opportunity_score"] = (
        opportunities["rating"] * 100
        +
        opportunities["review_count"] / 100
        -
        opportunities["price"] / 50
    )

    opportunities = opportunities.sort_values(
        "opportunity_score",
        ascending=False
    )

    return opportunities[
        [
            "keyword",
            "product_name",
            "price",
            "rating",
            "review_count",
            "opportunity_score"
        ]
    ]