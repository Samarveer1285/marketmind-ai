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

st.title("📋 Executive Summary")

brand_health = get_brand_health()
leaderboard = get_market_leaderboard()
opportunity = get_revenue_opportunity()
growth = get_brand_growth()

# ---------------------------

top_brand = brand_health.iloc[0]
top_product = leaderboard.iloc[0]
best_opportunity = opportunity.iloc[0]
fastest_brand = growth.iloc[0]

# ---------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏆 Top Brand",
        top_brand["brand"]
    )

with col2:
    st.metric(
        "⭐ Top Product",
        top_product["name"]
    )

with col3:
    st.metric(
        "💰 Best Opportunity",
        best_opportunity["name"]
    )

with col4:
    st.metric(
        "🚀 Fastest Growing Brand",
        fastest_brand["brand"]
    )

# ---------------------------

st.divider()

st.subheader("Executive Insights")

st.success(
    f"Top brand in the market is {top_brand['brand']}."
)

st.info(
    f"Highest ranked product is {top_product['name']}."
)

st.warning(
    f"Highest revenue opportunity is {best_opportunity['name']}."
)

st.success(
    f"Fastest growing brand is {fastest_brand['brand']}."
)

# ---------------------------

st.divider()

st.subheader("Top 5 Brands")

st.dataframe(
    brand_health.head(5)
)

st.subheader("Top 5 Products")

st.dataframe(
    leaderboard.head(5)
)