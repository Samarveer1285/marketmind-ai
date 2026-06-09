import streamlit as st

from analytics_function import load_data

from scenario_simulator import (
    simulate_price_change,
    simulate_rating_improvement,
    simulate_review_growth
)

st.set_page_config(
    layout="wide"
)

st.title(
    "🎯 Scenario Simulator"
)

products = sorted(
    load_data()["name"]
    .unique()
)

tab1, tab2, tab3 = st.tabs([
    "💰 Price Simulation",
    "⭐ Rating Simulation",
    "📈 Marketing Simulation"
])

with tab1:

    st.subheader(
        "Price Change Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="price_product"
    )

    price_change = st.slider(
        "Price Change %",
        -50,
        50,
        0
    )

    if st.button(
        "Run Price Simulation"
    ):

        result = (
            simulate_price_change(
                selected_product,
                price_change
            )
        )

        st.dataframe(
            result,
            use_container_width=True
        )

with tab2:

    st.subheader(
        "Rating Improvement Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="rating_product"
    )

    new_rating = st.slider(
        "Projected Rating",
        1.0,
        5.0,
        4.5,
        0.1
    )

    if st.button(
        "Run Rating Simulation"
    ):

        result = (
            simulate_rating_improvement(
                selected_product,
                new_rating
            )
        )

        st.dataframe(
            result,
            use_container_width=True
        )

with tab3:

    st.subheader(
        "Marketing Growth Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="marketing_product"
    )

    growth_pct = st.slider(
        "Review Growth %",
        0,
        200,
        20
    )

    if st.button(
        "Run Marketing Simulation"
    ):

        result = (
            simulate_review_growth(
                selected_product,
                growth_pct
            )
        )

        st.dataframe(
            result,
            use_container_width=True
        )