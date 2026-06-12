import streamlit as st
import plotly.express as px

from forecasting_v2 import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🤖 Forecasting V2"
)

results = compare_forecasting_models()

if results.empty:
    st.warning(
        "Not enough historical data available for forecasting."
    )
    st.stop()

st.subheader(
    "Model Comparison"
)

st.dataframe(
    results.sort_values(
        "linear_mae"
    ),
    use_container_width=True,
    hide_index=True
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
    text="count",
    title="Best Model Distribution"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="forecast_chart"
)