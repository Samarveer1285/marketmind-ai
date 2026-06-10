import streamlit as st
import plotly.express as px

from category_intelligence import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Category Intelligence",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

growth = get_category_growth()

market_share = get_category_market_share()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "📊 Category Intelligence",
    "Understand which categories drive the market."
)


# =====================================================
# PREP DATA
# =====================================================

growth = growth.copy()

market_share = market_share.copy()

category_summary = growth.merge(
    market_share,
    on="category",
    how="left"
)


# =====================================================
# TOP INSIGHTS
# =====================================================

top_growth = category_summary.sort_values(
    "growth_pct",
    ascending=False
).iloc[0]

top_share = category_summary.sort_values(
    "market_share",
    ascending=False
).iloc[0]

avg_growth = round(
    category_summary["growth_pct"].mean(),
    1
)

total_reviews = int(
    category_summary["review_count"].sum()
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
        "Fastest Category",
        top_growth["category"],
        f"{top_growth['growth_pct']:.1f}% growth"
    )


with col2:

    ui_components.executive_card(
        "🏆",
        "Largest Category",
        top_share["category"],
        f"{top_share['market_share']:.1f}% share"
    )


with col3:

    ui_components.executive_card(
        "📈",
        "Avg Growth",
        f"{avg_growth}%",
        "Across categories"
    )


with col4:

    ui_components.executive_card(
        "🛒",
        "Total Reviews",
        f"{total_reviews:,}",
        "Market activity"
    )


st.write("")
st.write("")


# =====================================================
# CATEGORY GROWTH + MARKET SHARE
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    growth_chart = px.bar(
        category_summary.sort_values(
            "growth_pct",
            ascending=True
        ),
        x="growth_pct",
        y="category",
        orientation="h",
        color="growth_pct",
        color_continuous_scale=[
            "#5AD7D1",
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
        xaxis_title="Growth %",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚀 Category Growth Leaders",
        growth_chart
    )


with right:

    donut = px.pie(
        market_share,
        names="category",
        values="market_share",
        hole=0.65,
        color_discrete_sequence=[
            "#8EF2C2",
            "#5AD7D1",
            "#60A5FA",
            "#A78BFA",
            "#F472B6"
        ]
    )

    donut.update_layout(
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
        "🏆 Category Market Share",
        donut
    )


st.write("")
st.write("")
# =====================================================
# CATEGORY POSITIONING MATRIX
# =====================================================

matrix_chart = px.scatter(
    category_summary,
    x="market_share",
    y="growth_pct",
    size="review_count",
    color="growth_pct",
    hover_name="category",
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
    xaxis_title="Market Share (%)",
    yaxis_title="Growth (%)"
)

ui_components.chart_card(
    "🎯 Category Positioning Matrix",
    matrix_chart
)


st.write("")
st.write("")


# =====================================================
# CATEGORY TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    growth_table = (
        category_summary
        .sort_values(
            "growth_pct",
            ascending=False
        )
        [
            [
                "category",
                "review_count_previous",
                "review_count_latest",
                "growth_pct"
            ]
        ]
    )

    ui_components.table_card(
        "🚀 Growth Rankings",
        growth_table
    )


with right:

    share_table = (
        category_summary
        .sort_values(
            "market_share",
            ascending=False
        )
        [
            [
                "category",
                "review_count",
                "market_share"
            ]
        ]
    )

    ui_components.table_card(
        "🏆 Market Share Rankings",
        share_table
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE CATEGORY BRIEF
# =====================================================

high_growth = (
    category_summary["growth_pct"] > avg_growth
).sum()

dominant_categories = (
    category_summary["market_share"] > 20
).sum()


ui_components.ai_brief_panel([
    f"{top_growth['category']} is the fastest-growing category with {top_growth['growth_pct']:.1f}% growth.",
    f"{top_share['category']} currently dominates with {top_share['market_share']:.1f}% market share.",
    f"{high_growth} categories are growing faster than the market average.",
    f"{dominant_categories} categories hold significant market concentration.",
    "Allocate resources toward high-growth categories while protecting established category leaders."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Category Growth Dataset"
):

    st.dataframe(
        growth,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Market Share Dataset"
):

    st.dataframe(
        market_share,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Combined Category Analysis"
):

    st.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Category Intelligence helps leadership identify emerging category opportunities and defend dominant positions using growth and market-share signals."
)