import pandas as pd

from analytics_function import *
from forecasting import *


def generate_recommendations():

    demand = get_demand_momentum()

    forecast = forecast_price()

    recommendations = []

    for _, row in demand.iterrows():

        product = row["name"]

        momentum = row["momentum_pct"]

        price_row = forecast[
            forecast["product"] == product
        ]

        future_price = (
            price_row["forecast_price"]
            .values[0]
        )

        if momentum > 20:

            action = (
                "Increase Marketing Budget"
            )

        elif momentum < -20:

            action = (
                "Demand Declining - Investigate"
            )

        else:

            action = (
                "Stable Performance"
            )

        priority_score = abs(momentum)

        recommendations.append({

            "product": product,

            "momentum": round(
                momentum,
                2
            ),

            "forecast_price":
                future_price,

            "priority_score":
                round(
                    priority_score,
                    2
                ),

            "recommendation":
                action
        })

    recommendations_df = pd.DataFrame(
        recommendations
    )

    return (
        recommendations_df
        .sort_values(
            by="priority_score",
            ascending=False
        )
    )
def get_risk_products():

    demand = get_demand_momentum()

    risk_products = demand.copy()

    risk_products["risk_score"] = (
        risk_products["momentum_pct"]
        .abs()
    )

    risk_products = (
        risk_products
        .sort_values(
            "risk_score",
            ascending=False
        )
    )

    return risk_products