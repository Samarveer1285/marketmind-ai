import streamlit as st
import plotly.express as px

from customer_segmentation import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

segments = get_customer_segments()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "👥 Customer Segmentation",
    "Understand customer personas and behavioral patterns."
)


# =====================================================
# SEGMENT INSIGHTS
# =====================================================

segment_summary = (
    segments
    .groupby("segment_name")
    .agg({
        "customer": "count",
        "price": "mean",
        "rating": "mean",
        "review_count": "mean"
    })
    .reset_index()
    .rename(columns={
        "customer": "customer_count",
        "price": "avg_price",
        "rating": "avg_rating",
        "review_count": "avg_reviews"
    })
)


largest_segment = (
    segment_summary
    .sort_values(
        "customer_count",
        ascending=False
    )
    .iloc[0]
)

highest_rated_segment = (
    segment_summary
    .sort_values(
        "avg_rating",
        ascending=False
    )
    .iloc[0]
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
        "👥",
    "Total Personas",
    len(segments),
    "Personas identified"
    )


with col2:

    ui_components.executive_card(
        "🧩",
        "Segments",
        segments["segment_name"].nunique(),
        "Customer personas"
    )


with col3:

    ui_components.executive_card(
        "🏆",
        "Largest Segment",
        largest_segment["segment_name"],
        f"{int(largest_segment['customer_count'])} products"
    )


with col4:

    ui_components.executive_card(
        "⭐",
        "Highest Rated",
        highest_rated_segment["segment_name"],
        f"{highest_rated_segment['avg_rating']:.2f} rating"
    )


st.write("")
st.write("")


# =====================================================
# SEGMENT DISTRIBUTION + CUSTOMER MATRIX
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    distribution_chart = px.pie(
        segment_summary,
        names="segment_name",
        values="customer_count",
        hole=0.65,
        color_discrete_sequence=[
            "#8EF2C2",
            "#5AD7D1",
            "#60A5FA",
            "#A78BFA",
            "#F472B6"
        ]
    )

    distribution_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    ui_components.chart_card(
        "📊 Segment Distribution",
        distribution_chart
    )


with right:

    scatter_data = segments.copy()

    scatter_data["rating"] = (
        scatter_data["rating"]
        .fillna(3)
    )

    scatter_data["review_count"] = (
        scatter_data["review_count"]
        .fillna(0)
    )

    scatter_data["price"] = (
        scatter_data["price"]
        .fillna(
            scatter_data["price"].median()
        )
    )

    customer_matrix = px.scatter(
        scatter_data,
        x="price",
        y="review_count",
        color="segment_name",
        size="rating",
        hover_name="customer"
    )

    customer_matrix.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Price Preference",
        yaxis_title="Review Activity"
    )

    ui_components.chart_card(
        "🎯 Customer Persona Matrix",
        customer_matrix
    )


st.write("")
st.write("")
# =====================================================
# SEGMENT RANKINGS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    segment_rankings = (
        segment_summary
        .sort_values(
            "customer_count",
            ascending=False
        )
        [
            [
                "segment_name",
                "customer_count",
                "avg_price",
                "avg_rating"
            ]
        ]
    )

    ui_components.table_card(
        "👥 Segment Rankings",
        segment_rankings
    )


with right:

    engagement_rankings = (
        segment_summary
        .sort_values(
            "avg_reviews",
            ascending=False
        )
        [
            [
                "segment_name",
                "avg_reviews",
                "avg_rating",
                "avg_price"
            ]
        ]
    )

    ui_components.table_card(
        "🔥 Engagement Rankings",
        engagement_rankings
    )


st.write("")
st.write("")


# =====================================================
# SEGMENT PROFILE TABLE
# =====================================================

segment_profiles = (
    segment_summary
    .copy()
)

segment_profiles["avg_price"] = (
    segment_profiles["avg_price"]
    .round(2)
)

segment_profiles["avg_rating"] = (
    segment_profiles["avg_rating"]
    .round(2)
)

segment_profiles["avg_reviews"] = (
    segment_profiles["avg_reviews"]
    .round(0)
)


ui_components.table_card(
    "🧩 Customer Segment Profiles",
    segment_profiles
)


st.write("")
st.write("")


# =====================================================
# EXECUTIVE CUSTOMER BRIEF
# =====================================================

premium_segments = (
    segment_summary["avg_price"]
    > segment_summary["avg_price"].mean()
).sum()

high_engagement_segments = (
    segment_summary["avg_reviews"]
    > segment_summary["avg_reviews"].mean()
).sum()


ui_components.ai_brief_panel([
    f"{largest_segment['segment_name']} is the largest customer persona with {int(largest_segment['customer_count'])} customers.",
    f"{highest_rated_segment['segment_name']} reports the strongest satisfaction at {highest_rated_segment['avg_rating']:.2f} stars.",
    f"{premium_segments} segments exhibit above-average spending preferences.",
    f"{high_engagement_segments} segments demonstrate above-average review engagement.",
    "Use segmentation insights to tailor pricing, promotions, and product positioning to distinct customer personas.",
    "Prioritize highly engaged segments for retention and advocacy initiatives."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Customer Segmentation Dataset"
):

    st.dataframe(
        segments,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Segment Summary"
):

    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Premium Customer Segments"
):

    premium_segment_names = (
        segment_summary[
            segment_summary["avg_price"]
            > segment_summary["avg_price"].mean()
        ]["segment_name"]
        .tolist()
    )

    premium_customers = (
        segments[
            segments["segment_name"]
            .isin(premium_segment_names)
        ]
    )

    st.dataframe(
        premium_customers,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Customer Segmentation transforms raw behavioral signals into actionable personas, enabling targeted growth, retention, and personalization strategies."
)