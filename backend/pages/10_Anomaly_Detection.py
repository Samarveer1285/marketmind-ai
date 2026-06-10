import streamlit as st
import plotly.express as px

from anomaly_detection import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Anomaly Detection",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

price_anomalies = detect_price_anomalies()

rating_anomalies = detect_rating_anomalies()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🚨 Anomaly Detection",
    "Detect unusual market behavior before it becomes a problem."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

largest_price = price_anomalies.iloc[
    price_anomalies["deviation_pct"]
    .abs()
    .idxmax()
]

largest_rating = rating_anomalies.iloc[
    rating_anomalies["deviation_pct"]
    .abs()
    .idxmax()
]

total_price_alerts = len(
    price_anomalies
)

total_rating_alerts = len(
    rating_anomalies
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
        "💰",
        "Biggest Price Anomaly",
        largest_price["product"],
        f"{largest_price['deviation_pct']:+.1f}% deviation"
    )


with col2:

    ui_components.executive_card(
        "⭐",
        "Biggest Rating Anomaly",
        largest_rating["product"],
        f"{largest_rating['deviation_pct']:+.1f}% deviation"
    )


with col3:

    ui_components.executive_card(
        "🚨",
        "Price Alerts",
        total_price_alerts,
        "Detected anomalies"
    )


with col4:

    ui_components.executive_card(
        "📣",
        "Rating Alerts",
        total_rating_alerts,
        "Detected anomalies"
    )


st.write("")
st.write("")


# =====================================================
# PRICE + RATING INTELLIGENCE
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    price_chart = px.bar(
        price_anomalies.assign(
            abs_dev=lambda x: x["deviation_pct"].abs()
        ).sort_values(
            "abs_dev",
            ascending=True
        ),
        x="deviation_pct",
        y="product",
        orientation="h",
        color="deviation_pct",
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
        xaxis_title="Price Deviation (%)",
        yaxis_title=""
    )

    ui_components.chart_card(
        "💰 Price Anomaly Intelligence",
        price_chart
    )


with right:

    rating_chart = px.bar(
        rating_anomalies.assign(
            abs_dev=lambda x: x["deviation_pct"].abs()
        ).sort_values(
            "abs_dev",
            ascending=True
        ),
        x="deviation_pct",
        y="product",
        orientation="h",
        color="deviation_pct",
        color_continuous_scale=[
            "#EF4444",
            "#F59E0B",
            "#8EF2C2"
        ]
    )

    rating_chart.update_layout(
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
        xaxis_title="Rating Deviation (%)",
        yaxis_title=""
    )

    ui_components.chart_card(
        "⭐ Rating Anomaly Intelligence",
        rating_chart
    )


st.write("")
st.write("")
# =====================================================
# DUAL ANOMALY MATRICES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    price_matrix = px.scatter(
        price_anomalies,
        x="average_price",
        y="latest_price",
        size=price_anomalies["deviation_pct"].abs(),
        color="deviation_pct",
        hover_name="product",
        color_continuous_scale=[
            "#EF4444",
            "#F59E0B",
            "#8EF2C2"
        ]
    )

    price_matrix.update_layout(
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
        xaxis_title="Average Price",
        yaxis_title="Latest Price"
    )

    ui_components.chart_card(
        "💰 Price Anomaly Matrix",
        price_matrix
    )


with right:

    rating_matrix = px.scatter(
        rating_anomalies,
        x="average_rating",
        y="latest_rating",
        size=rating_anomalies["deviation_pct"].abs(),
        color="deviation_pct",
        hover_name="product",
        color_continuous_scale=[
            "#EF4444",
            "#F59E0B",
            "#8EF2C2"
        ]
    )

    rating_matrix.update_layout(
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
        xaxis_title="Average Rating",
        yaxis_title="Latest Rating"
    )

    ui_components.chart_card(
        "⭐ Rating Anomaly Matrix",
        rating_matrix
    )


st.write("")
st.write("")


# =====================================================
# ANOMALY RANKINGS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    price_rankings = (
        price_anomalies
        .assign(
            anomaly_magnitude=lambda x: x["deviation_pct"].abs()
        )
        .sort_values(
            "anomaly_magnitude",
            ascending=False
        )
        [
            [
                "product",
                "latest_price",
                "average_price",
                "deviation_pct"
            ]
        ]
    )

    ui_components.table_card(
        "💰 Price Anomaly Rankings",
        price_rankings
    )


with right:

    rating_rankings = (
        rating_anomalies
        .assign(
            anomaly_magnitude=lambda x: x["deviation_pct"].abs()
        )
        .sort_values(
            "anomaly_magnitude",
            ascending=False
        )
        [
            [
                "product",
                "latest_rating",
                "average_rating",
                "deviation_pct"
            ]
        ]
    )

    ui_components.table_card(
        "⭐ Rating Anomaly Rankings",
        rating_rankings
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE ANOMALY BRIEF
# =====================================================

major_price_anomalies = (
    price_anomalies["deviation_pct"]
    .abs()
    > 10
).sum()

major_rating_anomalies = (
    rating_anomalies["deviation_pct"]
    .abs()
    > 10
).sum()


ui_components.ai_brief_panel([
    f"{largest_price['product']} exhibits the most significant pricing anomaly at {largest_price['deviation_pct']:+.1f}%.",
    f"{largest_rating['product']} demonstrates the largest rating anomaly at {largest_rating['deviation_pct']:+.1f}%.",
    f"{major_price_anomalies} products show pricing deviations greater than 10%.",
    f"{major_rating_anomalies} products show rating deviations greater than 10%.",
    "Persistent anomalies may indicate supply disruptions, sudden demand shifts, data quality issues, or emerging market opportunities.",
    "Products appearing consistently in anomaly reports should be prioritized for executive review."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Price Anomalies"
):

    st.dataframe(
        price_anomalies,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Rating Anomalies"
):

    st.dataframe(
        rating_anomalies,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Combined Anomaly Snapshot"
):

    combined_snapshot = (
        price_anomalies
        .rename(
            columns={
                "latest_price": "latest_value",
                "average_price": "average_value"
            }
        )
        .assign(
            anomaly_type="Price"
        )
    )

    rating_snapshot = (
        rating_anomalies
        .rename(
            columns={
                "latest_rating": "latest_value",
                "average_rating": "average_value"
            }
        )
        .assign(
            anomaly_type="Rating"
        )
    )

    anomaly_snapshot = pd.concat(
        [
            combined_snapshot,
            rating_snapshot
        ],
        ignore_index=True
    )

    st.dataframe(
        anomaly_snapshot,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Anomaly Detection continuously monitors market signals to surface unusual pricing and customer sentiment patterns before they materially impact business performance."
)