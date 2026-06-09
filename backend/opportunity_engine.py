from analytics_function import *

import pandas as pd


def get_opportunity_scores():

    momentum = get_demand_momentum()

    risk = get_risk_products()

    merged = momentum.merge(
        risk,
        on="name"
    )

    merged["opportunity_score"] = (

        (merged["momentum_pct"] * 0.7)

        +

        ((100 - merged["risk_score"]) * 0.3)

    )

    return (

        merged.sort_values(
            "opportunity_score",
            ascending=False
        )

    )


def get_top_opportunities():

    return (
        get_opportunity_scores()
        .head(20)
    )