import plotly.express as px
import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from analytics_function import *

st.set_page_config(layout="wide")

st.title("📈 Growth Analytics")

momentum = get_demand_momentum()
review_growth = get_review_growth()
risk = get_risk_products()
brand_growth = get_brand_growth()

st.subheader("🚀 Demand Momentum")
st.dataframe(momentum)
fig1 = px.bar(
    momentum.head(10),
    x="name",
    y="momentum_pct",
    title="Top Demand Momentum Products"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("⭐ Review Growth")
st.dataframe(review_growth)
fig2 = px.bar(
    review_growth.head(10),
    x="name",
    y="momentum_pct",
    title="Review Growth Ranking"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("⚠️ Risk Products")
st.dataframe(risk)
fig3 = px.scatter(
    risk,
    x="risk_score",
    y="avg_rating",
    hover_name="name",
    title="Risk Products Analysis"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("📊 Brand Growth")
st.dataframe(brand_growth)
fig4 = px.bar(
    brand_growth,
    x="brand",
    y="brand_growth_score",
    title="Brand Growth Score"
)

st.plotly_chart(fig4, use_container_width=True)
