from market_monitor import get_latest_market_data
import pandas as pd


def get_portfolio_scores():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    portfolio = data.copy()

    portfolio["momentum_pct"] = (
        portfolio["review_count"]
        /
        portfolio["review_count"].sum()
        * 100
    )

    portfolio["risk_score"] = (
        (5 - portfolio["rating"]) * 20
        -
        portfolio["review_count"] / 1000
    )

    portfolio["portfolio_score"] = (
        portfolio["rating"] * 25
        +
        portfolio["review_count"] / 500
        -
        portfolio["price"] / 1000
    )

    portfolio = portfolio.dropna(
        subset=[
            "rating",
            "review_count",
            "price"
        ]
    )

    if "product_name" in portfolio.columns:
        portfolio = portfolio.rename(
            columns={
                "product_name": "name"
            }
        )

    return portfolio.sort_values(
        "portfolio_score",
        ascending=False
    )


def get_invest_products():

    portfolio = get_portfolio_scores()

    return portfolio.head(10)


def get_exit_products():

    portfolio = get_portfolio_scores()

    return portfolio.sort_values(
        "risk_score",
        ascending=False
    ).head(10)