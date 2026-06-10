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


st.set_page_config(
    page_title="Market Intelligence",
    layout="wide"
)

apply_theme()


# ======================================================
# DATA
# ======================================================

leaderboard = get_market_leaderboard()

hidden_gems = get_hidden_gems()

opportunity = get_opportunity_matrix()

trust = get_customer_trust()


# ======================================================
# PAGE HEADER
# ======================================================

ui_components.page_header(
    "🧠 Market Intelligence",
    "Track leaders, opportunities and customer trust signals."
)


# ======================================================
# KPI SECTION
# ======================================================

top_market = leaderboard.iloc[0]

top_trust = trust.iloc[0]

star_count = (
    opportunity["category"] == "Star"
).sum()


col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:
    ui_components.executive_card(
        "🏆",
        "Market Leader",
        top_market["name"],
        f"Score: {top_market['market_score']:.1f}"
    )

with col2:
    ui_components.executive_card(
        "💎",
        "Hidden Gems",
        len(hidden_gems),
        "Undervalued Products"
    )

with col3:
    ui_components.executive_card(
        "🎯",
        "Star Opportunities",
        star_count,
        "High Potential"
    )

with col4:
    ui_components.executive_card(
        "🤝",
        "Highest Trust",
        top_trust["name"],
        f"Trust: {top_trust['trust_score']:.1f}"
    )


st.divider()


# ======================================================
# MARKET PERFORMANCE + CATEGORY SPLIT
# ======================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)

with left:

    ui_components.section_header(
        "📈",
        "Market Leaders"
    )

    fig1 = px.bar(
        leaderboard.head(10).sort_values(
            "market_score",
            ascending=True
        ),
        x="market_score",
        y="name",
        orientation="h",
        color="market_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Market Score",
        yaxis_title=""
    )

    ui_components.chart_card(
        "",
        fig1
    )


with right:

    ui_components.section_header(
        "🧩",
        "Opportunity Distribution"
    )

    category_split = (
        opportunity["category"]
        .value_counts()
        .reset_index()
    )

    category_split.columns = [
        "category",
        "count"
    ]

    donut = px.pie(
        category_split,
        names="category",
        values="count",
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
        "",
        donut
    )


st.divider()


# ======================================================
# OPPORTUNITY EXPLORER
# ======================================================

ui_components.section_header(
    "🎯",
    "Opportunity Explorer"
)

bubble = px.scatter(
    opportunity,
    x="review_count",
    y="rating",
    size="review_count",
    color="category",
    hover_name="name",
    color_discrete_sequence=[
        "#8EF2C2",
        "#5AD7D1",
        "#60A5FA",
        "#A78BFA",
        "#F472B6"
    ]
)

bubble.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    ),
    xaxis_title="Review Count",
    yaxis_title="Rating"
)

ui_components.chart_card(
    "",
    bubble
)


st.divider()


# ======================================================
# HIDDEN GEMS + TRUST TABLES
# ======================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    gems_display = hidden_gems[
        [
            "name",
            "rating",
            "review_count"
        ]
    ].head(10)

    ui_components.table_card(
        "💎 Hidden Gem Candidates",
        gems_display
    )


with right:

    trust_display = trust[
        [
            "name",
            "trust_score"
        ]
    ].head(10)

    ui_components.table_card(
        "🤝 Customer Trust Leaders",
        trust_display
    )


st.divider()


# ======================================================
# EXECUTIVE INSIGHTS
# ======================================================

ui_components.ai_brief_panel([
    f"{top_market['name']} currently leads overall market performance.",
    f"{len(hidden_gems)} products qualify as hidden opportunities.",
    f"{star_count} products are classified as Star performers.",
    f"{top_trust['name']} has the strongest customer trust score."
])


# ======================================================
# EXPANDABLE RAW DATA
# ======================================================

with st.expander("📋 View Full Market Leaderboard"):
    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )

with st.expander("📋 View Hidden Gems Dataset"):
    st.dataframe(
        hidden_gems,
        use_container_width=True,
        hide_index=True
    )

with st.expander("📋 View Opportunity Dataset"):
    st.dataframe(
        opportunity,
        use_container_width=True,
        hide_index=True
    )

with st.expander("📋 View Customer Trust Dataset"):
    st.dataframe(
        trust,
        use_container_width=True,
        hide_index=True
    )