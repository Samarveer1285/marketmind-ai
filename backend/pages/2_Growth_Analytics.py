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
    page_title="Growth Analytics",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

momentum = get_demand_momentum()

review_growth = get_review_growth()

risk = get_risk_products()

brand_growth = get_brand_growth()


# =====================================================
# PAGE HEADER
# =====================================================

ui_components.page_header(
    "📈 Growth Analytics",
    "Track accelerating demand, emerging risks, and growth leaders."
)


# =====================================================
# KPI SECTION
# =====================================================

top_momentum = momentum.iloc[0]

top_review = review_growth.iloc[0]

top_risk = risk.iloc[0]

top_brand = brand_growth.iloc[0]


col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:
    ui_components.executive_card(
        "🚀",
        "Demand Leader",
        top_momentum["name"],
        f"{top_momentum['momentum_pct']:.0f}% momentum"
    )

with col2:
    ui_components.executive_card(
        "⭐",
        "Review Leader",
        top_review["name"],
        f"{top_review['momentum_pct']:.0f}% growth"
    )

with col3:
    ui_components.executive_card(
        "⚠️",
        "Highest Risk",
        top_risk["name"],
        f"Risk Score {top_risk['risk_score']:.1f}"
    )

with col4:
    ui_components.executive_card(
        "🏆",
        "Growth Brand",
        top_brand["brand"],
        f"{top_brand['growth_pct']:.0f}% growth"
    )


st.write("")
st.write("")


# =====================================================
# DEMAND MOMENTUM + REVIEW GROWTH
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    momentum_chart = px.bar(
        momentum.head(10).sort_values(
            "momentum_pct",
            ascending=True
        ),
        x="momentum_pct",
        y="name",
        orientation="h",
        color="momentum_pct",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    momentum_chart.update_layout(
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
        xaxis_title="Momentum %",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚀 Demand Momentum Leaders",
        momentum_chart
    )


with right:

    review_chart = px.bar(
        review_growth.head(10).sort_values(
            "momentum_pct",
            ascending=True
        ),
        x="momentum_pct",
        y="name",
        orientation="h",
        color="momentum_pct",
        color_continuous_scale=[
            "#60A5FA",
            "#A78BFA"
        ]
    )

    review_chart.update_layout(
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
        xaxis_title="Review Growth %",
        yaxis_title=""
    )

    ui_components.chart_card(
        "⭐ Review Growth Leaders",
        review_chart
    )


st.write("")
st.write("")
# =====================================================
# RISK ANALYSIS + BRAND GROWTH
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
        "⚠️ Product Risk Analysis",
        risk_chart
    )


with right:

    brand_chart = px.bar(
        brand_growth.head(10).sort_values(
            "brand_growth_score",
            ascending=True
        ),
        x="brand_growth_score",
        y="brand",
        orientation="h",
        color="brand_growth_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    brand_chart.update_layout(
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
        xaxis_title="Growth Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🏆 Brand Growth Leaders",
        brand_chart
    )


st.write("")
st.write("")


# =====================================================
# TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    ui_components.table_card(
        "🚀 Top Demand Momentum",
        momentum.head(10)
    )

    ui_components.table_card(
        "⚠️ Highest Risk Products",
        risk.head(10)
    )


with right:

    ui_components.table_card(
        "⭐ Top Review Growth",
        review_growth.head(10)
    )

    ui_components.table_card(
        "🏆 Brand Growth Rankings",
        brand_growth.head(10)
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE GROWTH BRIEF
# =====================================================

ui_components.ai_brief_panel([
    f"{top_momentum['name']} is experiencing the fastest demand acceleration ({top_momentum['momentum_pct']:.0f}%).",
    f"{top_review['name']} is leading review growth trends.",
    f"{top_risk['name']} currently carries the highest risk score ({top_risk['risk_score']:.1f}).",
    f"{top_brand['brand']} is the strongest growth brand with {top_brand['growth_pct']:.0f}% growth."
])


# =====================================================
# RAW DATA EXPANDERS
# =====================================================

with st.expander("📋 View Full Demand Momentum Dataset"):

    st.dataframe(
        momentum,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Review Growth Dataset"):

    st.dataframe(
        review_growth,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Risk Dataset"):

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Brand Growth Dataset"):

    st.dataframe(
        brand_growth,
        use_container_width=True,
        hide_index=True
    )