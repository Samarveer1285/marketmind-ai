from langchain.tools import Tool

from analytics_function import (
    get_demand_momentum,
    get_brand_growth
)

from recommendation_engine import (
    generate_recommendations,
    get_risk_products
)

from category_intelligence import (
    get_category_growth
)


def demand_tool():

    data = get_demand_momentum()

    leader = data.iloc[0]

    return (
        f"Fastest growing product is "
        f"{leader['name']} "
        f"with growth "
        f"{round(leader['momentum_pct'],2)}%"
    )


def brand_tool():

    data = get_brand_growth()

    leader = data.iloc[0]

    return (
        f"Fastest growing brand is "
        f"{leader['brand']} "
        f"with growth "
        f"{round(leader['growth_pct'],2)}%"
    )


def recommendation_tool():

    data = generate_recommendations()

    leader = data.iloc[0]

    return (
        f"Best opportunity product is "
        f"{leader['name']}"
    )


def risk_tool():

    data = get_risk_products()

    leader = data.iloc[0]

    return (
        f"Highest risk product is "
        f"{leader['name']}"
    )


def category_tool():

    data = get_category_growth()

    leader = data.iloc[0]

    return (
        f"Fastest growing category is "
        f"{leader['category']}"
    )


tools = [

    Tool(
        name="Demand Growth Tool",
        func=lambda x: demand_tool(),
        description=(
            "Use when user asks about "
            "fastest growing products"
        )
    ),

    Tool(
        name="Brand Growth Tool",
        func=lambda x: brand_tool(),
        description=(
            "Use when user asks about "
            "brands"
        )
    ),

    Tool(
        name="Recommendation Tool",
        func=lambda x: recommendation_tool(),
        description=(
            "Use when user asks "
            "investment opportunities"
        )
    ),

    Tool(
        name="Risk Tool",
        func=lambda x: risk_tool(),
        description=(
            "Use when user asks "
            "risk related questions"
        )
    ),

    Tool(
        name="Category Tool",
        func=lambda x: category_tool(),
        description=(
            "Use when user asks "
            "category growth"
        )
    )
]