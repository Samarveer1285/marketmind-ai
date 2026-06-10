import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from forecasting import *
import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Forecasting Engine",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

forecast_df = forecast_reviews()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🔮 Forecasting Engine",
    "Predict future demand before the market reacts."
)


# =====================================================
# PREP DATA
# =====================================================

forecast_matrix = forecast_df.copy()

forecast_matrix["Growth"] = (
    forecast_matrix["forecast_reviews"]
    - forecast_matrix["current_reviews"]
)

forecast_matrix["Growth %"] = (
    (
        forecast_matrix["Growth"]
        / forecast_matrix["current_reviews"]
    ) * 100
).round(1)

forecast_matrix["Bubble_Size"] = (
    forecast_matrix["Growth"]
    .abs()
    + 10
)


# =====================================================
# KPI SECTION
# =====================================================

top_forecast = forecast_matrix.sort_values(
    "forecast_reviews",
    ascending=False
).iloc[0]


highest_growth = forecast_matrix.sort_values(
    "Growth",
    ascending=False
).iloc[0]


avg_current = int(
    forecast_matrix["current_reviews"].mean()
)


avg_forecast = int(
    forecast_matrix["forecast_reviews"].mean()
)


col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)


with col1:

    ui_components.executive_card(
        "🔮",
        "Top Forecast",
        top_forecast["product"],
        f"{int(top_forecast['forecast_reviews'])} future reviews"
    )


with col2:

    ui_components.executive_card(
        "🚀",
        "Highest Growth",
        highest_growth["product"],
        f"+{int(highest_growth['Growth'])} reviews"
    )


with col3:

    ui_components.executive_card(
        "📊",
        "Avg Current",
        avg_current,
        "Current review volume"
    )


with col4:

    ui_components.executive_card(
        "📈",
        "Avg Forecast",
        avg_forecast,
        "Expected review volume"
    )


st.write("")
st.write("")


# =====================================================
# CURRENT VS FORECAST
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    comparison_chart = go.Figure()

    comparison_chart.add_trace(
        go.Bar(
            name="Current",
            x=forecast_matrix["product"],
            y=forecast_matrix["current_reviews"]
        )
    )

    comparison_chart.add_trace(
        go.Bar(
            name="Forecast",
            x=forecast_matrix["product"],
            y=forecast_matrix["forecast_reviews"]
        )
    )

    comparison_chart.update_layout(
        barmode="group",
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="",
        yaxis_title="Reviews"
    )

    ui_components.chart_card(
        "📊 Current vs Forecast",
        comparison_chart
    )


with right:

    growth_chart = px.bar(
        forecast_matrix.sort_values(
            "Growth",
            ascending=True
        ),
        x="Growth",
        y="product",
        orientation="h",
        color="Growth",
        color_continuous_scale=[
            "#EF4444",
            "#F59E0B",
            "#8EF2C2"
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
        xaxis_title="Review Change",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚀 Forecast Growth Leaders",
        growth_chart
    )


st.write("")
st.write("")
# =====================================================
# FORECAST OPPORTUNITY MATRIX
# =====================================================

matrix_chart = px.scatter(
    forecast_matrix,
    x="current_reviews",
    y="forecast_reviews",
    size="Bubble_Size",
    color="Growth",
    hover_name="product",
    color_continuous_scale=[
        "#EF4444",
        "#F59E0B",
        "#8EF2C2"
    ]
)

matrix_chart.update_layout(
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
    xaxis_title="Current Reviews",
    yaxis_title="Forecast Reviews"
)

ui_components.chart_card(
    "🎯 Forecast Opportunity Matrix",
    matrix_chart
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

    top_growth = (
        forecast_matrix
        .sort_values(
            "Growth",
            ascending=False
        )
        .head(10)
        [
            [
                "product",
                "current_reviews",
                "forecast_reviews",
                "Growth"
            ]
        ]
    )

    ui_components.table_card(
        "🚀 Highest Forecast Growth",
        top_growth
    )


with right:

    forecast_leaders = (
        forecast_matrix
        .sort_values(
            "forecast_reviews",
            ascending=False
        )
        .head(10)
        [
            [
                "product",
                "forecast_reviews",
                "Growth %"
            ]
        ]
    )

    ui_components.table_card(
        "🔮 Forecast Leaders",
        forecast_leaders
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE FORECAST BRIEF
# =====================================================

positive_forecasts = (
    forecast_matrix["Growth"] > 0
).sum()

negative_forecasts = (
    forecast_matrix["Growth"] < 0
).sum()


ui_components.ai_brief_panel([
    f"{top_forecast['product']} is projected to achieve the highest future engagement.",
    f"{highest_growth['product']} shows the strongest expected acceleration.",
    f"{positive_forecasts} products are forecasted to gain momentum.",
    f"{negative_forecasts} products may experience declining engagement.",
    "Use forecast signals to prioritize inventory, marketing, and resource allocation."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Forecast Dataset"
):

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Forecast Analysis"
):

    st.dataframe(
        forecast_matrix,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Forecasts are directional estimates generated by MarketMind AI and should support, not replace, executive decision-making."
)