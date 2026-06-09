import streamlit as st
import plotly.express as px

from anomaly_detection_ml import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🤖 ML Anomaly Detection"
)

anomalies = (
    detect_ml_anomalies()
)

st.subheader(
    "Detected Anomalies"
)

st.dataframe(
    anomalies,
    use_container_width=True
)

fig = px.scatter(

    anomalies,

    x="price",

    y="review_count",

    hover_name="name",

    title="ML Detected Anomalies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)