import streamlit as st

from portfolio_optimizer import *

st.set_page_config(
    layout="wide"
)

st.title(
    "💼 Portfolio Optimizer"
)

invest = (
    get_invest_products()
)

exit_products = (
    get_exit_products()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Products To Invest In"
    )

    st.dataframe(
        invest,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Products To Consider Exiting"
    )

    st.dataframe(
        exit_products,
        use_container_width=True
    )