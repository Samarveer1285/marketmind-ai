import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from forecasting import *

st.set_page_config(layout="wide")

st.title("🔮 Forecasting Engine")

forecast_df = forecast_reviews()

st.subheader(
    "Future Review Forecast"
)

st.dataframe(
    forecast_df
)

fig = px.bar(
    forecast_df,
    x="product",
    y="forecast_reviews",
    title="Predicted Future Reviews"
)

st.plotly_chart(
    fig,
    use_container_width=True
)