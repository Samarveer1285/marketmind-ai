from market_monitor import get_latest_market_data


def get_executive_metrics():

    data = get_latest_market_data()

    if data.empty:
        return {
            "Total Products": 0,
            "Total Brands": 0,
            "Top Growth Product": "-",
            "Top Opportunity": "-",
            "Highest Risk Product": "-",
            "Top Category": "-"
        }

    total_products = data["title"].nunique()

    total_brands = data["brand"].nunique()

    top_growth_product = (
        data.sort_values(
            "review_count",
            ascending=False
        )
        .iloc[0]["title"]
    )

    opportunity = data.copy()

    opportunity["opportunity_score"] = (
        opportunity["rating"] * 100
        +
        opportunity["review_count"] / 100
        -
        opportunity["price"] / 50
    )

    top_opportunity = (
        opportunity.sort_values(
            "opportunity_score",
            ascending=False
        )
        .iloc[0]["title"]
    )

    risk = data.copy()

    risk["risk_score"] = (
        5 - risk["rating"]
    )

    highest_risk = (
        risk.sort_values(
            "risk_score",
            ascending=False
        )
        .iloc[0]["title"]
    )

    top_category = (
        data["category"]
        .value_counts()
        .index[0]
    )

    return {

        "Total Products":
            total_products,

        "Total Brands":
            total_brands,

        "Top Growth Product":
            top_growth_product,

        "Top Opportunity":
            top_opportunity,

        "Highest Risk Product":
            highest_risk,

        "Top Category":
            top_category
    }