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
    page_title="Brand Analytics",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

brand_health = get_brand_health()

brand_growth = get_brand_growth()


# =====================================================
# PAGE HEADER
# =====================================================

ui_components.page_header(
    "🏆 Brand Analytics",
    "Monitor brand strength and momentum across the market."
)


# =====================================================
# KPI SECTION
# =====================================================

top_health = brand_health.iloc[0]

top_growth = brand_growth.iloc[0]

avg_health = round(
    brand_health["brand_health_score"].mean(),
    1
)

avg_growth = round(
    brand_growth["brand_growth_score"].mean(),
    1
)

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:
    ui_components.executive_card(
        "🏆",
        "Health Leader",
        top_health["brand"],
        f"Score: {top_health['brand_health_score']:.1f}"
    )

with col2:
    ui_components.executive_card(
        "📈",
        "Growth Leader",
        top_growth["brand"],
        f"Score: {top_growth['brand_growth_score']:.1f}"
    )

with col3:
    ui_components.executive_card(
        "💚",
        "Avg Health",
        avg_health,
        "Market benchmark"
    )

with col4:
    ui_components.executive_card(
        "🚀",
        "Avg Growth",
        avg_growth,
        "Growth benchmark"
    )


st.write("")
st.write("")


# =====================================================
# BRAND HEALTH + GROWTH
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
        "🏅 Brand Health Leaders",
        health_chart
    )


with right:

    growth_chart = px.bar(
        brand_growth.head(10).sort_values(
            "brand_growth_score",
            ascending=True
        ),
        x="brand_growth_score",
        y="brand",
        orientation="h",
        color="brand_growth_score",
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
        xaxis_title="Growth Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "📈 Brand Growth Leaders",
        growth_chart
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
        "🏅 Top Brand Health Rankings",
        brand_health.head(10)
    )


with right:

    ui_components.table_card(
        "🚀 Top Brand Growth Rankings",
        brand_growth.head(10)
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE BRAND BRIEF
# =====================================================

ui_components.ai_brief_panel([
    f"{top_health['brand']} currently leads overall brand health.",
    f"{top_growth['brand']} is showing the strongest growth momentum.",
    f"Average market health stands at {avg_health}.",
    f"Average brand growth remains stable at {avg_growth}."
])


# =====================================================
# RAW DATA EXPANDERS
# =====================================================

with st.expander("📋 View Full Brand Health Dataset"):

    st.dataframe(
        brand_health,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Brand Growth Dataset"):

    st.dataframe(
        brand_growth,
        use_container_width=True,
        hide_index=True
    )