import streamlit as st
import plotly.express as px

from opportunity_engine import *

st.set_page_config(
    layout="wide"
)

st.title(
    "🎯 Opportunity Scoring"
)

opportunities = (
    get_top_opportunities()
)

st.subheader(
    "Top Opportunities"
)

st.dataframe(
    opportunities,
    use_container_width=True
)

fig = px.bar(
    opportunities.head(15),
    x="name",
    y="opportunity_score",
    title="Opportunity Score Ranking"
)

st.plotly_chart(
    fig,
    use_container_width=True
)