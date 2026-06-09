import streamlit as st
import plotly.express as px

from forecasting_v2 import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🤖 Forecasting V2"
)

results = (
    compare_forecasting_models()
)

st.subheader(
    "Model Comparison"
)

st.dataframe(
    results,
    use_container_width=True
)

best_models = (
    results[
        "best_model"
    ]
    .value_counts()
    .reset_index()
)

best_models.columns = [
    "model",
    "count"
]

fig = px.bar(

    best_models,

    x="model",

    y="count",

    title="Best Model Distribution"

)

st.plotly_chart(
    fig,
    use_container_width=True
)