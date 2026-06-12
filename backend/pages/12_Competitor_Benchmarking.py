import streamlit as st
import plotly.express as px
from live_competitor_benchmark import (
    get_live_brand_benchmark,
    get_live_category_leaders
)

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Competitor Benchmarking",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================
benchmark = get_live_brand_benchmark()

leaders = get_live_category_leaders()
if benchmark.empty or leaders.empty:

    st.warning(
        "No live market data available. "
        "Run the ingestion pipeline first."
    )

    st.stop()


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🏆 Competitor Benchmarking",
    "Track how competitors stack up across the market."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

best_competitor = benchmark.sort_values(
    "benchmark_score",
    ascending=False
).iloc[0]

highest_rated = benchmark.sort_values(
    "avg_rating",
    ascending=False
).iloc[0]

most_reviewed = benchmark.sort_values(
    "total_reviews",
    ascending=False
).iloc[0]

category_leader_count = leaders["category"].nunique()


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
        "Best Competitor",
        best_competitor["brand"],
        f"Score {best_competitor['benchmark_score']:.1f}"
    )


with col2:

    ui_components.executive_card(
        "⭐",
        "Highest Rated",
        highest_rated["brand"],
        f"{highest_rated['avg_rating']:.2f} rating"
    )


with col3:

    ui_components.executive_card(
        "🛒",
        "Most Reviewed",
        most_reviewed["brand"],
        f"{int(most_reviewed['total_reviews']):,} reviews"
    )


with col4:

    ui_components.executive_card(
        "👑",
        "Category Leaders",
        category_leader_count,
        "Winning categories"
    )


st.write("")
st.write("")


# =====================================================
# BRAND LEADERS + CATEGORY LEADERS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    benchmark_chart = px.bar(
        benchmark.sort_values(
            "benchmark_score",
            ascending=True
        ),
        x="benchmark_score",
        y="brand",
        orientation="h",
        color="benchmark_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    benchmark_chart.update_layout(
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
        xaxis_title="Benchmark Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🏆 Brand Benchmark Leaders",
        benchmark_chart
    )


with right:
    print(benchmark.columns.tolist())
    print(benchmark.columns.duplicated())

    print(leaders.columns.tolist())
    print(leaders.columns.duplicated())

    st.write(leaders.columns.tolist())
    st.write(leaders.columns.duplicated())
    category_chart = px.bar(
        leaders,
        x="review_count",
        y="category",
        color="brand",
        orientation="h"
    )

    category_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Review Count",
        yaxis_title=""
    )

    ui_components.chart_card(
        "👑 Category Leaders",
        category_chart
    )


st.write("")
st.write("")
# =====================================================
# COMPETITIVE POSITIONING MATRIX
# =====================================================

positioning_chart = px.scatter(
    benchmark,
    x="avg_price",
    y="avg_rating",
    size="total_reviews",
    color="benchmark_score",
    hover_name="brand",
    color_continuous_scale=[
        "#EF4444",
        "#F59E0B",
        "#8EF2C2"
    ]
)

positioning_chart.update_layout(
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
    yaxis_title="Average Rating"
)

ui_components.chart_card(
    "🎯 Competitive Positioning Matrix",
    positioning_chart
)


st.write("")
st.write("")


# =====================================================
# COMPETITOR TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    benchmark_rankings = (
        benchmark
        .sort_values(
            "benchmark_score",
            ascending=False
        )
        [
            [
                "brand",
                "avg_rating",
                "total_reviews",
                "avg_price",
                "benchmark_score"
            ]
        ]
    )

    ui_components.table_card(
        "🏆 Benchmark Rankings",
        benchmark_rankings
    )


with right:

    category_leaders = (
        leaders
        .sort_values(
            "review_count",
            ascending=False
        )
        [
            [
                "category",
                "brand",
                "review_count"
            ]
        ]
    )

    ui_components.table_card(
        "👑 Category Leadership",
        category_leaders
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE COMPETITIVE BRIEF
# =====================================================

premium_brands = (
    benchmark["avg_price"]
    > benchmark["avg_price"].mean()
).sum()

high_performers = (
    benchmark["benchmark_score"]
    > benchmark["benchmark_score"].mean()
).sum()


ui_components.ai_brief_panel([
    f"{best_competitor['brand']} currently leads the competitive landscape with a benchmark score of {best_competitor['benchmark_score']:.1f}.",
    f"{highest_rated['brand']} delivers the strongest customer satisfaction at {highest_rated['avg_rating']:.2f} stars.",
    f"{most_reviewed['brand']} commands the largest customer attention with {int(most_reviewed['total_reviews']):,} reviews.",
    f"{high_performers} brands outperform the market benchmark average.",
    f"{premium_brands} brands compete in the premium pricing segment.",
    "Use competitor intelligence to identify differentiation opportunities and defend market positioning."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Brand Benchmark Dataset"
):

    st.dataframe(
        benchmark,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Category Leaders Dataset"
):

    st.dataframe(
        leaders,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Competitive Intelligence Snapshot"
):

    competitive_snapshot = benchmark.merge(
        leaders,
        on="brand",
        how="left"
    )

    st.dataframe(
        competitive_snapshot,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Competitor Benchmarking enables leadership teams to track market leaders, identify differentiation opportunities, and strengthen competitive positioning."
)