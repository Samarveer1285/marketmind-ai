from analytics_function import *
from opportunity_engine import *
from category_intelligence import *


def get_executive_metrics():

    merged = load_data()

    total_products = (
        merged["name"]
        .nunique()
    )

    total_brands = (
        merged["brand"]
        .nunique()
    )

    top_growth_product = (
        get_demand_momentum()
        .iloc[0]["name"]
    )

    top_opportunity = (
        get_top_opportunities()
        .iloc[0]["name"]
    )

    highest_risk = (
        get_risk_products()
        .iloc[0]["name"]
    )

    top_category = (
        get_category_growth()
        .iloc[0]["category"]
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