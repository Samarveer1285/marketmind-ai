from analytics_function import *
from recommendation_engine import *


def answer_question(question):

    question = question.lower()

    recommendations = (
        generate_recommendations()
    )

    if (
        "marketing" in question
        or
        "recommend" in question
    ):

        top_product = recommendations.iloc[0]

        return f"""
Recommended Product:

{top_product['product']}

Priority Score:

{round(top_product['priority_score'],2)}

Suggested Action:

{top_product['recommendation']}
"""

    elif (
        "risk" in question
        or
        "risky" in question
    ):

        risk = get_risk_products()

        top_risk = risk.iloc[0]

        return f"""
Highest Risk Product:

{top_risk['name']}

Risk Score:

{round(top_risk['risk_score'],2)}
"""

    elif (
        "brand" in question
        or
        "company" in question
    ):

        brand = get_brand_growth()

        leader = brand.iloc[0]

        return f"""
Fastest Growing Brand:

{leader['brand']}

Growth Score:

{round(leader['brand_growth_score'],2)}
"""

    elif (
        "grow" in question
        or
        "growing" in question
        or
        "momentum" in question
    ):

        momentum = get_demand_momentum()

        leader = momentum.iloc[0]

        return f"""
Fastest Growing Product:

{leader['name']}

Growth:

{round(leader['momentum_pct'],2)}%
"""

    else:

        return """
Try asking:

- Which product is growing?
- Which brand is growing?
- Which product deserves marketing?
- Which product is risky?
"""