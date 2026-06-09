import streamlit as st

from executive_scorecard import *

st.set_page_config(
    layout="wide"
)

st.title(
    "📈 Executive KPI Scorecard"
)

metrics = (
    get_executive_metrics()
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Products",
        metrics[
            "Total Products"
        ]
    )

    st.metric(
        "Top Growth Product",
        metrics[
            "Top Growth Product"
        ]
    )

with col2:

    st.metric(
        "Total Brands",
        metrics[
            "Total Brands"
        ]
    )

    st.metric(
        "Top Opportunity",
        metrics[
            "Top Opportunity"
        ]
    )

with col3:

    st.metric(
        "Highest Risk Product",
        metrics[
            "Highest Risk Product"
        ]
    )

    st.metric(
        "Top Category",
        metrics[
            "Top Category"
        ]
    )