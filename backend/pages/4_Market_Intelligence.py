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

st.set_page_config(layout="wide")

st.title("🧠 Market Intelligence")

leaderboard = get_market_leaderboard()
gems = get_hidden_gems()
opportunity = get_opportunity_matrix()
trust = get_customer_trust()

# --------------------------------------------------

st.subheader("🏆 Market Leaderboard")

st.dataframe(leaderboard)

fig1 = px.bar(
    leaderboard,
    x="name",
    y="market_score",
    title="Market Score Ranking"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# --------------------------------------------------

st.subheader("💎 Hidden Gems")

st.dataframe(gems)

fig2 = px.scatter(
    gems,
    x="review_count",
    y="rating",
    hover_name="name",
    title="Hidden Gems"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------------------------

st.subheader("🎯 Opportunity Matrix")

st.dataframe(opportunity)

fig3 = px.scatter(
    opportunity,
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

# --------------------------------------------------

st.subheader("🤝 Customer Trust Score")

st.dataframe(
    trust.head(20)
)

fig4 = px.bar(
    trust.head(10),
    x="name",
    y="trust_score",
    title="Top Customer Trust Products"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)