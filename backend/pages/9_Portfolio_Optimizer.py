import streamlit as st
import plotly.express as px
import pandas as pd

from portfolio_optimizer import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Portfolio Optimizer",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

invest = get_invest_products()

exit_products = get_exit_products()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "💼 Portfolio Optimizer",
    "Transform market signals into investment decisions."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

best_investment = invest.sort_values(
    "portfolio_score",
    ascending=False
).iloc[0]

highest_exit = exit_products.sort_values(
    "risk_score",
    ascending=False
).iloc[0]

avg_invest_score = round(
    invest["portfolio_score"].mean(),
    1
)

avg_exit_score = round(
    exit_products["portfolio_score"].mean(),
    1
)


# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:

    ui_components.executive_card(
        "🚀",
        "Best Investment",
        best_investment["name"],
        f"Score {best_investment['portfolio_score']:.1f}"
    )


with col2:

    ui_components.executive_card(
        "⚠️",
        "Highest Exit Risk",
        highest_exit["name"],
        f"Risk {highest_exit['risk_score']:.1f}"
    )


with col3:

    ui_components.executive_card(
        "📈",
        "Avg Invest Score",
        avg_invest_score,
        "Investment basket"
    )


with col4:

    ui_components.executive_card(
        "📉",
        "Avg Exit Score",
        avg_exit_score,
        "Exit basket"
    )


st.write("")
st.write("")


# =====================================================
# INVEST VS EXIT CHARTS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    invest_chart = px.bar(
        invest.sort_values(
            "portfolio_score",
            ascending=True
        ),
        x="portfolio_score",
        y="name",
        orientation="h",
        color="portfolio_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    invest_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Portfolio Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚀 Investment Priorities",
        invest_chart
    )


with right:

    exit_chart = px.bar(
        exit_products.sort_values(
            "risk_score",
            ascending=True
        ),
        x="risk_score",
        y="name",
        orientation="h",
        color="risk_score",
        color_continuous_scale=[
            "#F97316",
            "#EF4444"
        ]
    )

    exit_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Risk Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "⚠️ Exit Priorities",
        exit_chart
    )


st.write("")
st.write("")
# =====================================================
# PORTFOLIO MATRIX
# =====================================================

portfolio_matrix = px.scatter(
    invest,
    x="risk_score",
    y="momentum_pct",
    size="portfolio_score",
    color="portfolio_score",
    hover_name="name",
    color_continuous_scale=[
        "#5AD7D1",
        "#8EF2C2"
    ]
)

portfolio_matrix.update_layout(
    title=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    ),
    xaxis_title="Risk Score",
    yaxis_title="Momentum (%)"
)

ui_components.chart_card(
    "🎯 Investment Opportunity Matrix",
    portfolio_matrix
)


st.write("")
st.write("")


# =====================================================
# PORTFOLIO TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    invest_rankings = (
        invest
        .sort_values(
            "portfolio_score",
            ascending=False
        )
        [
            [
                "name",
                "momentum_pct",
                "avg_rating",
                "risk_score",
                "portfolio_score"
            ]
        ]
    )

    ui_components.table_card(
        "🚀 Invest Rankings",
        invest_rankings
    )


with right:

    exit_rankings = (
        exit_products
        .sort_values(
            "risk_score",
            ascending=False
        )
        [
            [
                "name",
                "momentum_pct",
                "avg_rating",
                "risk_score",
                "portfolio_score"
            ]
        ]
    )

    ui_components.table_card(
        "⚠️ Exit Rankings",
        exit_rankings
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE PORTFOLIO BRIEF
# =====================================================

high_conviction = (
    invest["portfolio_score"] > avg_invest_score
).sum()

critical_exits = (
    exit_products["risk_score"]
    > exit_products["risk_score"].mean()
).sum()


ui_components.ai_brief_panel([
    f"{best_investment['name']} is the strongest investment candidate with a portfolio score of {best_investment['portfolio_score']:.1f}.",
    f"{highest_exit['name']} represents the highest-risk asset requiring immediate review.",
    f"{high_conviction} products exceed the average investment threshold.",
    f"{critical_exits} products fall into the elevated-risk zone.",
    "Reallocate resources toward high-momentum, low-risk products while reducing exposure to deteriorating assets."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Investment Candidates"
):

    st.dataframe(
        invest,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Exit Candidates"
):

    st.dataframe(
        exit_products,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Combined Portfolio Snapshot"
):

    combined = invest.copy()

    combined["Decision"] = "Invest"

    exits = exit_products.copy()

    exits["Decision"] = "Exit"

    portfolio_snapshot = pd.concat(
        [combined, exits],
        ignore_index=True
    )

    st.dataframe(
        portfolio_snapshot,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Portfolio Optimizer converts analytical signals into actionable capital allocation decisions for executive teams."
)