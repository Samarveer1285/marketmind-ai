import streamlit as st

from recommendation_engine import generate_recommendations
from anomaly_detection import get_risk_products
from forecasting import forecast_reviews
from forecasting import forecast_price
from market_alerts import generate_market_alerts
from analytics_function import get_demand_momentum


st.title(
    "🎯 Executive Command Center"
)

# -----------------------------
# TOP KPIs
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

growth = get_demand_momentum()

fastest_product = growth.iloc[0]

risk = get_risk_products()

highest_risk = risk.iloc[0]

alerts = generate_market_alerts()

recommendations = generate_recommendations()

top_opportunity = recommendations.iloc[0]

with col1:

    st.metric(
        "Fastest Growing Product",
        fastest_product["name"]
    )

with col2:

    st.metric(
        "Highest Risk Product",
        highest_risk["name"]
    )

with col3:

    st.metric(
        "Active Alerts",
        len(alerts)
    )

with col4:

    st.metric(
        "Top Opportunity",
        top_opportunity["product"]
    )

# -----------------------------
# ALERTS
# -----------------------------

st.subheader(
    "🚨 Critical Alerts"
)

st.dataframe(
    alerts.head(10),
    use_container_width=True
)

# -----------------------------
# OPPORTUNITIES
# -----------------------------

st.subheader(
    "💰 Top Opportunities"
)

st.dataframe(
    recommendations.head(10),
    use_container_width=True
)

# -----------------------------
# RISKS
# -----------------------------

st.subheader(
    "⚠️ Highest Risk Products"
)

st.dataframe(
    risk.head(10),
    use_container_width=True
)

# -----------------------------
# FORECASTS
# -----------------------------

st.subheader(
    "📈 Future Demand Forecast"
)

review_forecasts = forecast_reviews()
price_forecasts = forecast_price()

st.write("### Review Forecasts")

st.dataframe(
    review_forecasts,
    use_container_width=True
)

st.write("### Price Forecasts")

st.dataframe(
    price_forecasts,
    use_container_width=True
)

st.success(
    "Executive Summary Generated Successfully"
)