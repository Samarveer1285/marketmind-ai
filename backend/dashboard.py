import plotly.express as px
import streamlit as st

from analytics_function import *

st.set_page_config(
    page_title="MarketMind AI",
    layout="wide"
)

st.title("📊 MarketMind AI")
st.subheader("AI Powered Market Intelligence Platform")

# LOAD DATA

brand_health = get_brand_health()
leaderboard = get_market_leaderboard()
opportunities = get_revenue_opportunity()
hidden_gems = get_hidden_gems()

# KPI SECTION

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Top Brand",
        brand_health.iloc[0]["brand"]
    )

with col2:
    st.metric(
        "Top Product",
        leaderboard.iloc[0]["name"]
    )

with col3:
    st.metric(
        "Best Opportunity",
        opportunities.iloc[0]["name"]
    )

with col4:
    st.metric(
        "Hidden Gems",
        len(hidden_gems)
    )

st.divider()

# TABLES

st.subheader("🏆 Brand Health Ranking")
st.dataframe(brand_health)
fig = px.bar(
    brand_health,
    x="brand",
    y="brand_health_score",
    title="Brand Health Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📈 Market Leaderboard")
st.dataframe(leaderboard)
fig2 = px.bar(
    leaderboard,
    x="name",
    y="market_score",
    title="Market Leaderboard"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("💎 Hidden Gems")
st.dataframe(hidden_gems)
matrix = get_opportunity_matrix()

fig3 = px.scatter(
    matrix,
    x="review_count",
    y="rating",
    color="category",
    hover_name="name",
    size="review_count",
    title="Opportunity Matrix"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)