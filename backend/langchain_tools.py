from langchain.tools import Tool
from recommendation_engine import get_risk_products
from live_dashboard_analytics import (
    get_live_demand_momentum,
    get_live_brand_health,
    get_live_market_leaderboard,
    get_live_opportunity_matrix
)

from market_monitor import get_latest_market_data

def demand_tool():

    data = get_live_demand_momentum().head(5)

    response = "Top momentum brands:\n\n"

    for i, (_, row) in enumerate(data.iterrows(), start=1):

        response += (
            f"{i}. {row['brand']}\n"
            f"   Momentum: {row['momentum_pct']:.1f}%\n\n"
        )

    response += (
        "These brands are accelerating fastest "
        "based on recent market momentum."
    )

    return response

def brand_tool():

    data = (
        get_live_brand_health()
        .sort_values(
            "brand_health_score",
            ascending=False
        )
        .head(5)
    )

    response = "Strongest brands currently are:\n\n"

    for i, (_, row) in enumerate(data.iterrows(), start=1):

        response += (
            f"{i}. {row['brand']}\n"
            f"   Health Score: {row['brand_health_score']:.1f}\n\n"
        )

    response += (
        "These brands demonstrate the strongest "
        "overall market health."
    )

    return response


def recommendation_tool():

    data = get_live_market_leaderboard().head(5)

    response = "Top market opportunities:\n\n"

    for i, (_, row) in enumerate(data.iterrows(), start=1):

        response += (
            f"{i}. {row['name']}\n"
            f"   Brand: {row['brand']}\n"
        )

        if "market_score" in row:
            response += (
                f"   Market Score: "
                f"{row['market_score']:.1f}\n"
            )

        response += "\n"

    response += (
        "These products currently represent "
        "the strongest investment opportunities."
    )

    return response


def risk_tool():

    data = get_risk_products()

    top5 = data.head(5)

    response = "Highest risk products currently are:\n\n"

    for i, (_, row) in enumerate(top5.iterrows(), start=1):

        response += (
            f"{i}. {row['name']}\n"
            f"   Start Reviews: {int(row['start_reviews'])}\n"
            f"   End Reviews: {int(row['end_reviews'])}\n"
            f"   Momentum: {row['momentum_pct']:.1f}%\n"
            f"   Risk Score: {row['risk_score']:.2f}\n\n"
        )

    response += (
        "These products show the highest risk scores "
        "based on demand momentum behaviour."
    )

    return response



def category_tool():

    data = (
        get_latest_market_data()
        .groupby("category")
        .size()
        .reset_index(name="products")
        .sort_values(
            "products",
            ascending=False
        )
        .head(5)
    )

    response = "Leading categories are:\n\n"

    for i, (_, row) in enumerate(data.iterrows(), start=1):

        response += (
            f"{i}. {row['category']}\n"
            f"   Products Tracked: "
            f"{int(row['products'])}\n\n"
        )

    response += (
        "These categories dominate the "
        "current market landscape."
    )

    return response


tools = [

    Tool(
        name="Demand Growth Tool",
        func=lambda x: demand_tool(),
        description="Use for questions about fastest growing brands, momentum leaders, and demand acceleration."
    ),

    Tool(
        name="Brand Growth Tool",
        func=lambda x: brand_tool(),
        description="Use for questions about strongest brands, healthiest brands, and brand performance."
    ),

    Tool(
        name="Recommendation Tool",
        func=lambda x: recommendation_tool(),
        description="Use for questions about opportunities, investments, recommendations, and top products."
    ),

    Tool(
        name="Risk Tool",
        func=lambda x: risk_tool(),
       description="Use for questions about risky products, underperformers, and products requiring attention."
    ),

    Tool(
        name="Category Tool",
        func=lambda x: category_tool(),
        description="Use for questions about categories, category dominance, and category performance."
    )
]