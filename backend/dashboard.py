import streamlit as st

st.set_page_config(
    page_title="MarketMind Home",
    layout="wide"
)

import plotly.express as px

from analytics_function import (
    get_brand_health,
    get_market_leaderboard,
    get_revenue_opportunity,
    get_hidden_gems,
    get_opportunity_matrix
)

import ui_components
from theme import apply_theme


# ====================================
# THEME
# ====================================

apply_theme()


# ====================================
# LOAD DATA
# ====================================

brand_health = get_brand_health()

leaderboard = get_market_leaderboard()

opportunities = get_revenue_opportunity()

hidden_gems = get_hidden_gems()

matrix = get_opportunity_matrix()


# ====================================
# HEADER
# ====================================

ui_components.page_header(
    "🏠 MarketMind AI",
    "Executive Intelligence Platform for E-commerce Decision Making"
)

st.markdown(
    """
    ### Predict • Detect • Simulate • Recommend • Act
    """
)

st.caption(
    "20+ Intelligence Modules • Gemini AI • ML Surveillance • Decision Intelligence"
)

st.write("")
st.write("")


# ====================================
# EXECUTIVE SNAPSHOT
# ====================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    ui_components.executive_card(
        "🏆",
        "Market Leader",
        brand_health.iloc[0]["brand"],
        "Highest Brand Health"
    )

with col2:

    ui_components.executive_card(
        "📡",
        "Top Product",
        leaderboard.iloc[0]["name"],
        "Leading Market Score"
    )

with col3:

    ui_components.executive_card(
        "💎",
        "Opportunity",
        opportunities.iloc[0]["name"],
        "Highest Potential"
    )

with col4:

    ui_components.executive_card(
        "🧩",
        "Hidden Gems",
        len(hidden_gems),
        "Undervalued Products"
    )


st.write("")
st.write("")


# ====================================
# MARKET PERFORMANCE + CATEGORY SPLIT
# ====================================

left, right = st.columns([2, 1])

with left:

    fig = px.bar(
        brand_health.head(10),
        x="brand",
        y="brand_health_score",
        color="brand_health_score",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        title=None
    )

    ui_components.chart_card(
        "📈 Market Performance",
        fig
    )


with right:

    category_split = (
        matrix["category"]
        .value_counts()
        .reset_index()
    )

    category_split.columns = [
        "category",
        "count"
    ]

    donut = px.pie(
        category_split,
        values="count",
        names="category",
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
        ),
        legend_title=None
    )

    ui_components.chart_card(
        "🧩 Category Split",
        donut
    )


st.write("")
st.write("")


# ====================================
# TOP BRANDS + AI BRIEF
# ====================================

left, right = st.columns([2, 1])

with left:

    ui_components.table_card(
        "🏆 Top Brand Rankings",
        brand_health.head(10)
    )


with right:

    ui_components.ai_brief_panel([
        f"{brand_health.iloc[0]['brand']} leads overall brand performance.",
        f"{leaderboard.iloc[0]['name']} dominates the market leaderboard.",
        f"{len(hidden_gems)} hidden opportunities deserve investigation.",
        "Market conditions remain stable across major categories."
    ])


st.write("")
st.write("")
# ====================================
# OPPORTUNITY EXPLORER
# ====================================

fig2 = px.scatter(
    matrix,
    x="review_count",
    y="rating",
    size="review_count",
    color="category",
    hover_name="name"
)

fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    ),
    title=None
)

ui_components.chart_card(
    "🎯 Opportunity Explorer",
    fig2
)


st.write("")
st.write("")


# ====================================
# PLATFORM CAPABILITIES
# ====================================

st.subheader(
    "🚀 Platform Capabilities"
)

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:

    ui_components.executive_card(
        "🔮",
        "Forecasting",
        "Enabled",
        "Predict future demand"
    )

with row1_col2:

    ui_components.executive_card(
        "🤖",
        "AI Copilot",
        "Gemini",
        "Natural language insights"
    )

with row1_col3:

    ui_components.executive_card(
        "🎮",
        "Simulator",
        "Ready",
        "Test business scenarios"
    )


row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:

    ui_components.executive_card(
        "🚨",
        "ML Surveillance",
        "Active",
        "Detect market anomalies"
    )

with row2_col2:

    ui_components.executive_card(
        "🎯",
        "Opportunity Engine",
        "Operational",
        "Surface growth bets"
    )

with row2_col3:

    ui_components.executive_card(
        "👥",
        "Segmentation",
        "Available",
        "Understand personas"
    )


st.write("")
st.write("")


# ====================================
# ARCHITECTURE
# ====================================

st.subheader(
    "🏗 Platform Architecture"
)

st.info(
    """
Flipkart Integration (Upcoming)

⬇

Analytics Engines

⬇

ML Models

⬇

Gemini Copilot

⬇

Executive Dashboards

⬇

Business Decisions
"""
)


st.write("")
st.write("")


# ====================================
# TECH STACK
# ====================================

st.subheader(
    "🛠 Technology Stack"
)

tech1, tech2, tech3, tech4, tech5, tech6 = st.columns(6)

with tech1:

    ui_components.executive_card(
        "🐍",
        "Python",
        "Core",
        "Backend"
    )

with tech2:

    ui_components.executive_card(
        "🎈",
        "Streamlit",
        "UI",
        "Frontend"
    )

with tech3:

    ui_components.executive_card(
        "📊",
        "Plotly",
        "Charts",
        "Visual Analytics"
    )

with tech4:

    ui_components.executive_card(
        "🐼",
        "Pandas",
        "Data",
        "Processing"
    )

with tech5:

    ui_components.executive_card(
        "🧠",
        "Scikit-Learn",
        "ML",
        "Predictive Models"
    )

with tech6:

    ui_components.executive_card(
        "✨",
        "Gemini",
        "AI",
        "Decision Support"
    )


st.write("")
st.write("")


# ====================================
# PRODUCT ROADMAP
# ====================================

st.subheader(
    "🗺 Product Roadmap"
)

roadmap_left, roadmap_right = st.columns(2)

with roadmap_left:

    ui_components.ai_brief_panel([
        "✅ Executive Analytics",
        "✅ Forecasting Engine",
        "✅ Scenario Simulation",
        "✅ ML Surveillance",
        "✅ AI Copilot"
    ])


with roadmap_right:

    ui_components.ai_brief_panel([
        "⬜ Flipkart Integration",
        "⬜ Real-Time Updates",
        "⬜ LangChain Agent",
        "⬜ Tool Calling",
        "⬜ Context-Aware AI"
    ])


st.write("")
st.write("")


# ====================================
# FOOTER
# ====================================

st.divider()

st.caption(
    "Built by Samarveer Thakur • MarketMind AI v2.0 • Executive Intelligence Platform"
)