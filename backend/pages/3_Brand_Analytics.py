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

st.title("🏆 Brand Analytics")

brand_health = get_brand_health()
brand_growth = get_brand_growth()

st.subheader("🏅 Brand Health Ranking")
st.dataframe(brand_health)

fig1 = px.bar(
    brand_health,
    x="brand",
    y="brand_health_score",
    title="Brand Health Score"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Brand Growth")
st.dataframe(brand_growth)

fig2 = px.bar(
    brand_growth,
    x="brand",
    y="brand_growth_score",
    title="Brand Growth Score"
)

st.plotly_chart(fig2, use_container_width=True)
