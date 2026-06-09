from analytics_function import *
from recommendation_engine import *

import pandas as pd


def get_portfolio_scores():

    momentum = get_demand_momentum()

    risk = get_risk_products()

    merged = momentum.merge(
        risk,
        on="name"
    )

    merged[
        "portfolio_score"
    ] = (
        merged["momentum_pct"]
        -
        merged["risk_score"]
    )

    return (
        merged.sort_values(
            "portfolio_score",
            ascending=False
        )
    )


def get_invest_products():

    portfolio = (
        get_portfolio_scores()
    )

    return portfolio.head(10)


def get_exit_products():

    portfolio = (
        get_portfolio_scores()
    )

    return portfolio.tail(10)