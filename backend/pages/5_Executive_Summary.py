import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from analytics_function import *
import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Summary",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

brand_health = get_brand_health()

leaderboard = get_market_leaderboard()

opportunity = get_revenue_opportunity()

growth = get_brand_growth()


# =====================================================
# PAGE HEADER
# =====================================================

ui_components.page_header(
    "📋 Executive Summary",
    "One glance. One decision."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

top_brand = brand_health.iloc[0]

top_product = leaderboard.iloc[0]

best_opportunity = opportunity.iloc[0]

fastest_brand = growth.iloc[0]


# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:
    ui_components.executive_card(
        "🏆",
        "Top Brand",
        top_brand["brand"],
        f"Health Score: {top_brand['brand_health_score']:.1f}"
    )

with col2:
    ui_components.executive_card(
        "⭐",
        "Top Product",
        top_product["name"],
        f"Market Score: {top_product['market_score']:.1f}"
    )

with col3:
    ui_components.executive_card(
        "💰",
        "Best Opportunity",
        best_opportunity["name"],
        f"Opportunity: {best_opportunity['opportunity_score']:.1f}"
    )

with col4:
    ui_components.executive_card(
        "🚀",
        "Fastest Growing",
        fastest_brand["brand"],
        f"{fastest_brand['growth_pct']:.0f}% growth"
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE HIGHLIGHTS
# =====================================================

ui_components.ai_brief_panel([
    f"{top_brand['brand']} currently leads overall brand health.",
    f"{top_product['name']} remains the strongest market performer.",
    f"{best_opportunity['name']} presents the highest revenue opportunity.",
    f"{fastest_brand['brand']} is experiencing the strongest growth momentum."
])


st.write("")
st.write("")


# =====================================================
# TOP TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    ui_components.table_card(
        "🏆 Top 5 Brands",
        brand_health.head(5)
    )


with right:

    ui_components.table_card(
        "⭐ Top 5 Products",
        leaderboard.head(5)
    )


st.write("")
st.write("")
# =====================================================
# BRAND HEALTH + OPPORTUNITY LANDSCAPE
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

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
        "🏆 Brand Health Leaders",
        health_chart
    )


with right:

    opportunity_chart = px.scatter(
        opportunity.head(20),
        x="review_count",
        y="rating",
        size="opportunity_score",
        color="opportunity_score",
        hover_name="name",
        color_continuous_scale=[
            "#60A5FA",
            "#A78BFA"
        ]
    )

    opportunity_chart.update_layout(
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
        xaxis_title="Review Count",
        yaxis_title="Rating"
    )

    ui_components.chart_card(
        "💰 Opportunity Landscape",
        opportunity_chart
    )


st.write("")
st.write("")


# =====================================================
# CEO ACTION PANEL
# =====================================================

ui_components.ai_brief_panel([
    f"Protect and reinforce {top_brand['brand']}'s leadership position.",
    f"Capitalize on the momentum behind {top_product['name']}.",
    f"Prioritize investment opportunities around {best_opportunity['name']}.",
    f"Study the growth playbook of {fastest_brand['brand']} to replicate success.",
    "Maintain a balanced focus between short-term wins and long-term growth."
])


st.write("")
st.write("")


# =====================================================
# RAW DATA EXPANDERS
# =====================================================

with st.expander("📋 View Full Brand Health Dataset"):

    st.dataframe(
        brand_health,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Market Leaderboard"):

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Revenue Opportunity Dataset"):

    st.dataframe(
        opportunity,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Brand Growth Dataset"):

    st.dataframe(
        growth,
        use_container_width=True,
        hide_index=True
    )