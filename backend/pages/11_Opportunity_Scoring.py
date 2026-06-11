import streamlit as st
import plotly.express as px
from live_opportunity_page import generate_live_opportunities

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Opportunity Scoring",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

opportunities = generate_live_opportunities()
if opportunities.empty:

    st.warning(
        "No live market data available. "
        "Run the ingestion pipeline first."
    )

    st.stop()

# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🎯 Opportunity Scoring",
    "Prioritize the products with the highest strategic upside."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

top_opportunity = opportunities.sort_values(
    "opportunity_score",
    ascending=False
).iloc[0]

fastest_momentum = opportunities.sort_values(
    "momentum_pct",
    ascending=False
).iloc[0]

highest_rated = opportunities.sort_values(
    "avg_rating",
    ascending=False
).iloc[0]

avg_opportunity = round(
    opportunities["opportunity_score"].mean(),
    1
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
        "💎",
        "Top Opportunity",
        top_opportunity["name"],
        f"Score {top_opportunity['opportunity_score']:.1f}"
    )

with col2:

    ui_components.executive_card(
        "🚀",
        "Fastest Momentum",
        fastest_momentum["name"],
        f"{fastest_momentum['momentum_pct']:.1f}% growth"
    )

with col3:

    ui_components.executive_card(
        "⭐",
        "Highest Rated",
        highest_rated["name"],
        f"{highest_rated['avg_rating']:.2f} rating"
    )

with col4:

    ui_components.executive_card(
        "📈",
        "Avg Opportunity",
        avg_opportunity,
        "Market benchmark"
    )


st.write("")
st.write("")


# =====================================================
# OPPORTUNITY LEADERS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    opportunity_chart = px.bar(
        opportunities.sort_values(
            "opportunity_score",
            ascending=True
        ),
        x="opportunity_score",
        y="name",
        orientation="h",
        color="opportunity_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
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
        xaxis_title="Opportunity Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "💎 Opportunity Leaders",
        opportunity_chart
    )


with right:

    momentum_chart = px.scatter(
        opportunities,
        x="momentum_pct",
        y="opportunity_score",
        size="avg_rating",
        color="risk_score",
        hover_name="name",
        color_continuous_scale=[
            "#8EF2C2",
            "#F59E0B",
            "#EF4444"
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
        xaxis_title="Momentum (%)",
        yaxis_title="Opportunity Score"
    )

    ui_components.chart_card(
        "🚀 Momentum vs Opportunity",
        momentum_chart
    )


st.write("")
st.write("")
# =====================================================
# OPPORTUNITY MATRIX
# =====================================================

opportunity_matrix = px.scatter(
    opportunities,
    x="risk_score",
    y="momentum_pct",
    size="opportunity_score",
    color="opportunity_score",
    hover_name="name",
    color_continuous_scale=[
        "#EF4444",
        "#F59E0B",
        "#8EF2C2"
    ]
)

opportunity_matrix.update_layout(
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
    yaxis_title="Momentum (%)"
)

ui_components.chart_card(
    "🎯 Opportunity Matrix",
    opportunity_matrix
)


st.write("")
st.write("")


# =====================================================
# OPPORTUNITY RANKINGS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    opportunity_rankings = (
        opportunities
        .sort_values(
            "opportunity_score",
            ascending=False
        )
        [
            [
                "name",
                "momentum_pct",
                "avg_rating",
                "risk_score",
                "opportunity_score"
            ]
        ]
    )

    ui_components.table_card(
        "🏆 Opportunity Rankings",
        opportunity_rankings
    )


with right:

    momentum_rankings = (
        opportunities
        .sort_values(
            "momentum_pct",
            ascending=False
        )
        [
            [
                "name",
                "start_reviews",
                "end_reviews",
                "momentum_pct",
                "opportunity_score"
            ]
        ]
    )

    ui_components.table_card(
        "🚀 Momentum Rankings",
        momentum_rankings
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE OPPORTUNITY BRIEF
# =====================================================

high_confidence = (
    opportunities["opportunity_score"]
    > avg_opportunity
).sum()

low_risk = (
    opportunities["risk_score"]
    < opportunities["risk_score"].mean()
).sum()


ui_components.ai_brief_panel([
    f"{top_opportunity['name']} represents the strongest opportunity with a score of {top_opportunity['opportunity_score']:.1f}.",
    f"{fastest_momentum['name']} demonstrates the fastest acceleration at {fastest_momentum['momentum_pct']:.1f}% momentum.",
    f"{highest_rated['name']} combines strong customer satisfaction with growth potential.",
    f"{high_confidence} products exceed the average opportunity threshold.",
    f"{low_risk} products combine relatively lower risk with attractive upside.",
    "Prioritize products that balance momentum, customer satisfaction, and manageable risk."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Opportunity Dataset"
):

    st.dataframe(
        opportunities,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Top Opportunity Candidates"
):

    st.dataframe(
        opportunities
        .sort_values(
            "opportunity_score",
            ascending=False
        )
        .head(15),
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Low-Risk Opportunities"
):

    st.dataframe(
        opportunities[
            opportunities["risk_score"]
            < opportunities["risk_score"].mean()
        ].sort_values(
            "opportunity_score",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Opportunity Scoring helps leadership teams focus attention and resources on the products with the strongest potential upside."
)