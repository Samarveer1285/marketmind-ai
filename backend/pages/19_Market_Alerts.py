import streamlit as st

from market_alerts import generate_market_alerts


st.title(
    "🚨 Market Alert Center"
)

alerts = generate_market_alerts()

st.metric(
    "Active Alerts",
    len(alerts)
)

st.dataframe(
    alerts,
    use_container_width=True
)

st.warning(
    "Products listed here require immediate business attention."
)