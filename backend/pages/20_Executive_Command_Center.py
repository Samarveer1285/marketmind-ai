import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from recommendation_engine import generate_recommendations
from anomaly_detection import get_risk_products
from forecasting import forecast_reviews, forecast_price
from market_alerts import generate_market_alerts
from analytics_function import get_demand_momentum

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Command Center",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

growth = get_demand_momentum()

risk = get_risk_products()

alerts = generate_market_alerts()

recommendations = generate_recommendations()

review_forecasts = forecast_reviews()

price_forecasts = forecast_price()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🎯 Executive Command Center",
    "Mission control for executive decision-making."
)


# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

fastest_product = growth.iloc[0]

highest_risk = risk.iloc[0]

top_opportunity = recommendations.iloc[0]

active_alerts = len(alerts)


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
        "Fastest Growth",
        fastest_product["name"],
        f"{fastest_product['momentum_pct']:.0f}% momentum"
    )

with col2:

    ui_components.executive_card(
        "⚠️",
        "Highest Risk",
        highest_risk["name"],
        f"Risk Score {highest_risk['risk_score']:.1f}"
    )

with col3:

    ui_components.executive_card(
        "🚨",
        "Active Alerts",
        active_alerts,
        "Critical market signals"
    )

with col4:

    ui_components.executive_card(
        "💰",
        "Top Opportunity",
        top_opportunity["product"],
        f"Priority {top_opportunity['priority_score']:.1f}"
    )


st.write("")
st.write("")


# =====================================================
# MISSION CONTROL CHARTS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    momentum_chart = px.bar(
        growth.head(10).sort_values(
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
        "🚀 Demand Momentum Radar",
        momentum_chart
    )


with right:

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
        "⚠️ Risk Radar",
        risk_chart
    )


st.write("")
st.write("")
# =====================================================
# CRITICAL ALERTS + OPPORTUNITIES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    alerts_display = alerts.copy()

    ui_components.table_card(
        "🚨 Critical Alerts",
        alerts_display.head(10)
    )


with right:

    opportunity_display = (
        recommendations[
            [
                "product",
                "priority_score",
                "recommendation"
            ]
        ]
        .head(10)
    )

    ui_components.table_card(
        "💰 Top Opportunities",
        opportunity_display
    )


st.write("")
st.write("")


# =====================================================
# FORECAST INTELLIGENCE
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    review_chart = go.Figure()

    review_chart.add_trace(
        go.Bar(
            name="Current",
            x=review_forecasts["product"],
            y=review_forecasts["current_reviews"]
        )
    )

    review_chart.add_trace(
        go.Bar(
            name="Forecast",
            x=review_forecasts["product"],
            y=review_forecasts["forecast_reviews"]
        )
    )

    review_chart.update_layout(
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
        "📈 Future Demand Forecast",
        review_chart
    )


with right:

    price_forecasts["Price Change"] = (
        price_forecasts["forecast_price"]
        - price_forecasts["current_price"]
    )

    price_chart = px.bar(
        price_forecasts.sort_values(
            "Price Change",
            ascending=True
        ),
        x="Price Change",
        y="product",
        orientation="h",
        color="Price Change",
        color_continuous_scale=[
            "#EF4444",
            "#F59E0B",
            "#8EF2C2"
        ]
    )

    price_chart.update_layout(
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
        xaxis_title="Price Change",
        yaxis_title=""
    )

    ui_components.chart_card(
        "💵 Price Forecast Intelligence",
        price_chart
    )


st.write("")
st.write("")
# =====================================================
# EXECUTIVE AI BRIEF
# =====================================================

top_alert = (
    alerts.iloc[0]["message"]
    if len(alerts) > 0
    else "No critical alerts detected."
)

top_recommendation = (
    recommendations.iloc[0]["recommendation"]
)

highest_review_forecast = (
    review_forecasts.sort_values(
        "forecast_reviews",
        ascending=False
    )
    .iloc[0]
)

largest_price_shift = (
    price_forecasts.iloc[
        price_forecasts["Price Change"]
        .abs()
        .idxmax()
    ]
)


ui_components.ai_brief_panel([
    f"{fastest_product['name']} is currently the strongest growth signal in the market.",
    f"Immediate alert: {top_alert}",
    f"Priority action: {top_recommendation}",
    f"{highest_review_forecast['product']} is projected to receive the highest future engagement.",
    f"{largest_price_shift['product']} is expected to experience the largest price movement.",
    "Leadership teams should prioritize opportunities while actively mitigating emerging risks."
])


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
        "⚠️ Highest Risk Products",
        risk.head(10)
    )

    st.write("")

    ui_components.table_card(
        "🚀 Growth Leaders",
        growth.head(10)
    )


with right:

    ui_components.table_card(
        "📈 Review Forecasts",
        review_forecasts.head(10)
    )

    st.write("")

    ui_components.table_card(
        "💵 Price Forecasts",
        price_forecasts.head(10)
    )


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Market Alerts"
):

    st.dataframe(
        alerts,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Recommendation Engine Output"
):

    st.dataframe(
        recommendations,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Risk Analysis"
):

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Demand Momentum"
):

    st.dataframe(
        growth,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Review Forecasts"
):

    st.dataframe(
        review_forecasts,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Price Forecasts"
):

    st.dataframe(
        price_forecasts,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "MarketMind Executive Command Center consolidates opportunities, risks, alerts, and predictive intelligence into a single executive decision layer."
)