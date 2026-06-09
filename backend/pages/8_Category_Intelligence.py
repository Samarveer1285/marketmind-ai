import streamlit as st
import plotly.express as px

from category_intelligence import *

st.set_page_config(
    layout="wide"
)

st.title(
    "📊 Category Intelligence"
)

growth = (
    get_category_growth()
)

market_share = (
    get_category_market_share()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Fastest Growing Categories"
    )

    st.dataframe(
        growth,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Category Market Share"
    )

    fig = px.pie(
        market_share,
        names="category",
        values="market_share",
        title="Market Share by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader(
    "Category Leaderboard"
)

leaderboard = (
    market_share[
        [
            "category",
            "market_share"
        ]
    ]
)

st.dataframe(
    leaderboard,
    use_container_width=True
)