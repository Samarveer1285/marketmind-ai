import streamlit as st
import plotly.express as px

from product_segmentation import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🤖 Product Segmentation"
)

segments = (
    get_product_segments()
)

st.subheader(
    "Segmented Products"
)

st.dataframe(
    segments,
    use_container_width=True
)

fig = px.scatter(

    segments,

    x="price",

    y="review_count",

    color="segment",

    hover_name="name",

    title="Product Segments"

)

st.plotly_chart(
    fig,
    use_container_width=True
)