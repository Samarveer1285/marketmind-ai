import streamlit as st
import plotly.express as px

from customer_segmentation import *

st.set_page_config(
    layout="wide"
)

st.title(
    "👥 Customer Segmentation"
)

segments = (
    get_customer_segments()
)

st.subheader(
    "Customer Segments"
)

st.dataframe(
    segments,
    use_container_width=True
)

fig = px.scatter(

    segments,

    x="price",

    y="review_count",

    color="segment_name",

    hover_name="customer",

    title="Customer Segment Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)