import streamlit as st
import plotly.express as px

from competitor_benchmark import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🏆 Competitor Benchmarking"
)

benchmark = (
    get_brand_benchmark()
)

leaders = (
    get_category_leaders()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Brand Benchmark Ranking"
    )

    st.dataframe(
        benchmark,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Category Leaders"
    )

    st.dataframe(
        leaders,
        use_container_width=True
    )

st.divider()

fig = px.bar(

    benchmark.head(15),

    x="brand",

    y="benchmark_score",

    title="Top Brand Benchmark Scores"

)

st.plotly_chart(
    fig,
    use_container_width=True
)