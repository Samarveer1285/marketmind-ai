from analytics_function import *
from recommendation_engine import *


def answer_question(question):

    question = question.lower()

    if (
        "grow" in question
        or "growing" in question
        or "momentum" in question
    ):

        momentum = get_demand_momentum()

        leader = momentum.iloc[0]

        return f"""
Fastest Growing Product:

{leader['name']}

Growth:

{round(leader['momentum_pct'],2)}%
"""

    elif (
        "brand" in question
        and "grow" in question
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
        "marketing" in question
        or "recommend" in question
    ):

        recommendations = generate_recommendations()

        top = recommendations.iloc[0]

        return f"""
Recommended Product:

{top['product']}

Priority Score:

{top['priority_score']}

Action:

{top['recommendation']}
"""

    elif (
        "risk" in question
        or "risky" in question
    ):

        risk = get_risk_products()

        top = risk.iloc[0]

        return f"""
Highest Risk Product:

{top['name']}

Risk Score:

{round(top['risk_score'],2)}
"""

    elif (
        "hidden gem" in question
        or "underrated" in question
    ):

        gems = get_hidden_gems()

        top = gems.iloc[0]

        return f"""
Top Hidden Gem:

{top['name']}

Rating:

{round(top['rating'],2)}
"""

    elif (
        "undervalued" in question
        or "best value" in question
    ):

        value = get_undervalued_products()

        top = value.iloc[0]

        return f"""
Best Value Product:

{top['name']}

Value Score:

{round(top['value_score'],2)}
"""

    elif (
        "price drop" in question
        or "cheapest" in question
    ):

        drops = get_biggest_price_drops()

        top = drops.iloc[0]

        return f"""
Largest Price Drop:

{top['name']}

Price Change:

{round(top['price_change_pct'],2)}%
"""

    elif (
        "trust" in question
    ):

        trust = get_customer_trust()

        top = trust.iloc[0]

        return f"""
Most Trusted Product:

{top['name']}

Trust Score:

{round(top['trust_score'],2)}
"""

    else:

        return """
Try asking:

- Which product is growing?
- Which brand is growing?
- Which product deserves marketing?
- Which product is risky?
- Which product is undervalued?
- Which product is a hidden gem?
- Which product has highest trust?
- Which product had biggest price drop?
"""