import streamlit as st

from anomaly_detection import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🚨 Anomaly Detection"
)

price_anomalies = (
    detect_price_anomalies()
)

rating_anomalies = (
    detect_rating_anomalies()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Price Anomalies"
    )

    st.dataframe(
        price_anomalies,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Rating Anomalies"
    )

    st.dataframe(
        rating_anomalies,
        use_container_width=True
    )