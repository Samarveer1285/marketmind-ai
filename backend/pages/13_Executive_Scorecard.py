import streamlit as st
import plotly.express as px

from executive_scorecard import *
from analytics_function import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Scorecard",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

metrics = get_executive_metrics()

brand_health = get_brand_health()

brand_growth = get_brand_growth()

leaderboard = get_market_leaderboard()

risk = get_risk_products()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "📈 Executive Scorecard",
    "Executive pulse of the entire market."
)


# =====================================================
# EXECUTIVE KPI CARDS
# =====================================================

col1, col2, col3 = st.columns(
    3,
    gap="large"
)

with col1:

    ui_components.executive_card(
        "📦",
        "Total Products",
        metrics["Total Products"],
        "Products monitored"
    )

    st.write("")

    ui_components.executive_card(
        "🚀",
        "Top Growth Product",
        metrics["Top Growth Product"],
        "Fastest accelerator"
    )


with col2:

    ui_components.executive_card(
        "🏢",
        "Total Brands",
        metrics["Total Brands"],
        "Brands tracked"
    )

    st.write("")

    ui_components.executive_card(
        "💰",
        "Top Opportunity",
        metrics["Top Opportunity"],
        "Highest potential"
    )


with col3:

    ui_components.executive_card(
        "⚠️",
        "Highest Risk",
        metrics["Highest Risk Product"],
        "Needs attention"
    )

    st.write("")

    ui_components.executive_card(
        "🎧",
        "Top Category",
        metrics["Top Category"],
        "Leading segment"
    )


st.write("")
st.write("")


# =====================================================
# MARKET LEADERS + BRAND GROWTH
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    leader_chart = px.bar(
        leaderboard.head(10).sort_values(
            "market_score",
            ascending=True
        ),
        x="market_score",
        y="name",
        orientation="h",
        color="market_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    leader_chart.update_layout(
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
        xaxis_title="Market Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🏆 Market Leaders",
        leader_chart
    )


with right:

    growth_chart = px.bar(
        brand_growth.head(10).sort_values(
            "growth_pct",
            ascending=True
        ),
        x="growth_pct",
        y="brand",
        orientation="h",
        color="growth_pct",
        color_continuous_scale=[
            "#60A5FA",
            "#A78BFA"
        ]
    )

    growth_chart.update_layout(
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
        xaxis_title="Growth %",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚀 Brand Growth Leaders",
        growth_chart
    )


st.write("")
st.write("")
# =====================================================
# RISK + BRAND HEALTH
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    risk_chart = px.scatter(
        risk.head(20),
        x="risk_score",
        y="avg_rating",
        size="risk_score",
        color="risk_score",
        hover_name="name",
        color_continuous_scale=[
            "#F97316",
            "#EF4444"
        ]
    )

    risk_chart.update_layout(
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
        yaxis_title="Average Rating"
    )

    ui_components.chart_card(
        "⚠️ Risk Watchlist",
        risk_chart
    )


with right:

    health_chart = px.bar(
        brand_health.head(10).sort_values(
            "brand_health_score",
            ascending=True
        ),
        x="brand_health_score",
        y="brand",
        orientation="h",
        color="brand_health_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    health_chart.update_layout(
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
        xaxis_title="Health Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "💚 Brand Health Leaders",
        health_chart
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    ui_components.table_card(
        "🏆 Top Market Products",
        leaderboard.head(10)
    )

    st.write("")

    ui_components.table_card(
        "💚 Brand Health Rankings",
        brand_health.head(10)
    )


with right:

    ui_components.table_card(
        "🚀 Brand Growth Rankings",
        brand_growth.head(10)
    )

    st.write("")

    ui_components.table_card(
        "⚠️ Risk Products",
        risk.head(10)
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE ACTION BRIEF
# =====================================================

ui_components.ai_brief_panel([
    f"{metrics['Top Growth Product']} is currently driving market momentum.",
    f"{metrics['Top Opportunity']} represents the strongest investment opportunity.",
    f"{metrics['Highest Risk Product']} should be monitored closely due to elevated risk.",
    f"{metrics['Top Category']} remains the most dominant category.",
    f"The organization currently tracks {metrics['Total Products']} products across {metrics['Total Brands']} brands."
])


st.write("")
st.write("")


# =====================================================
# RAW DATA EXPANDERS
# =====================================================

with st.expander("📋 View Market Leaderboard"):

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Brand Health Dataset"):

    st.dataframe(
        brand_health,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Brand Growth Dataset"):

    st.dataframe(
        brand_growth,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Risk Dataset"):

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )