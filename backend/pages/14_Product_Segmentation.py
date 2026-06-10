import streamlit as st
import plotly.express as px

from product_segmentation import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Product Segmentation",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

segments = get_product_segments()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🤖 Product Segmentation",
    "Group products into meaningful strategic clusters."
)


# =====================================================
# SEGMENT INSIGHTS
# =====================================================

segment_summary = (
    segments
    .groupby("segment")
    .agg({
        "name": "count",
        "price": "mean",
        "rating": "mean",
        "review_count": "mean"
    })
    .reset_index()
    .rename(columns={
        "name": "product_count",
        "price": "avg_price",
        "rating": "avg_rating",
        "review_count": "avg_reviews"
    })
)


largest_segment = (
    segment_summary
    .sort_values(
        "product_count",
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
        "📦",
        "Total Products",
        len(segments),
        "Products analysed"
    )


with col2:

    ui_components.executive_card(
        "🧩",
        "Segments",
        segments["segment"].nunique(),
        "Product clusters"
    )


with col3:

    ui_components.executive_card(
        "🏆",
        "Largest Segment",
        f"Segment {int(largest_segment['segment'])}",
        f"{int(largest_segment['product_count'])} products"
    )


with col4:

    ui_components.executive_card(
        "⭐",
        "Highest Rated",
        f"Segment {int(highest_rated_segment['segment'])}",
        f"{highest_rated_segment['avg_rating']:.2f} rating"
    )


st.write("")
st.write("")


# =====================================================
# SEGMENT DISTRIBUTION + PRODUCT MATRIX
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    distribution_chart = px.pie(
        segment_summary,
        names="segment",
        values="product_count",
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
        "📊 Product Segment Distribution",
        distribution_chart
    )


with right:

    product_matrix = px.scatter(
        segments,
        x="price",
        y="review_count",
        color="segment",
        size="rating",
        hover_name="name"
    )

    product_matrix.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Price",
        yaxis_title="Review Count"
    )

    ui_components.chart_card(
        "🎯 Product Positioning Matrix",
        product_matrix
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
            "product_count",
            ascending=False
        )
        [
            [
                "segment",
                "product_count",
                "avg_price",
                "avg_rating"
            ]
        ]
    )

    ui_components.table_card(
        "📦 Segment Rankings",
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
                "segment",
                "avg_reviews",
                "avg_rating",
                "avg_price"
            ]
        ]
    )

    ui_components.table_card(
        "🔥 Popularity Rankings",
        engagement_rankings
    )


st.write("")
st.write("")


# =====================================================
# PRODUCT SEGMENT PROFILES
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
    "🧩 Product Segment Profiles",
    segment_profiles
)


st.write("")
st.write("")


# =====================================================
# EXECUTIVE PRODUCT BRIEF
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
    f"Segment {int(largest_segment['segment'])} is the largest cluster with {int(largest_segment['product_count'])} products.",
    f"Segment {int(highest_rated_segment['segment'])} achieves the strongest customer satisfaction at {highest_rated_segment['avg_rating']:.2f} stars.",
    f"{premium_segments} segments operate above the average pricing benchmark.",
    f"{high_engagement_segments} segments generate above-average customer engagement.",
    "Use product clusters to tailor pricing, promotions, and inventory strategies for different product archetypes.",
    "Prioritize highly rated and highly engaged segments when allocating growth investments."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Product Segmentation Dataset"
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
    "📋 View Premium Product Segments"
):

    premium_segment_ids = (
        segment_summary[
            segment_summary["avg_price"]
            > segment_summary["avg_price"].mean()
        ]["segment"]
        .tolist()
    )

    premium_products = (
        segments[
            segments["segment"]
            .isin(premium_segment_ids)
        ]
    )

    st.dataframe(
        premium_products,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Product Segmentation transforms product-level signals into strategic clusters, enabling differentiated pricing, assortment, and investment decisions."
)