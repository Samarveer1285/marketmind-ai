import streamlit as st
import plotly.express as px

from market_alerts import generate_market_alerts

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Market Alert Center",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

alerts = generate_market_alerts()

if alerts.empty:

    st.warning(
        "No market alerts generated from the latest live data."
    )

    st.stop()
# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🚨 Market Alert Center",
    "Monitor critical market signals requiring executive attention."
)


# =====================================================
# ALERT INSIGHTS
# =====================================================

total_alerts = len(
    alerts
)

unique_alert_types = alerts[
    "Type"
].nunique()

products_impacted = alerts[
    "Product"
].nunique()

most_common_alert = (
    alerts["Type"]
    .value_counts()
    .idxmax()
)

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:

    ui_components.executive_card(
        "🚨",
        "Active Alerts",
        total_alerts,
        "Open market alerts"
    )


with col2:

    ui_components.executive_card(
        "📌",
        "Alert Types",
        unique_alert_types,
        "Distinct categories"
    )


with col3:

    ui_components.executive_card(
        "📦",
        "Products Impacted",
        products_impacted,
        "Affected products"
    )


with col4:

    ui_components.executive_card(
        "⚠️",
        "Most Common",
        most_common_alert,
        "Dominant alert type"
    )


st.write("")
st.write("")


# =====================================================
# ALERT DISTRIBUTION
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    alert_distribution = (
        alerts["Type"]
        .value_counts()
        .reset_index()
    )

    alert_distribution.columns = [
        "type",
        "count"
    ]

    distribution_chart = px.pie(
        alert_distribution,
        names="type",
        values="count",
        hole=0.65,
        color_discrete_sequence=[
            "#EF4444",
            "#F59E0B",
            "#60A5FA",
            "#A78BFA",
            "#F472B6"
        ]
    )

    distribution_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    ui_components.chart_card(
        "📊 Alert Distribution",
        distribution_chart
    )


with right:

    alert_type_chart = px.bar(
        alert_distribution.sort_values(
            "count",
            ascending=True
        ),
        x="count",
        y="type",
        orientation="h",
        color="count",
        color_continuous_scale=[
            "#F59E0B",
            "#EF4444"
        ]
    )

    alert_type_chart.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Alert Count",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚨 Alert Intelligence",
        alert_type_chart
    )


st.write("")
st.write("")
# =====================================================
# PRIORITY ALERT TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    ui_components.table_card(
        "🚨 Active Market Alerts",
        alerts[
            [
                "Type",
                "Product",
                "Message"
            ]
        ]
    )


with right:

    alert_rankings = (
        alerts["Type"]
        .value_counts()
        .reset_index()
    )

    alert_rankings.columns = [
        "Alert Type",
        "Frequency"
    ]

    ui_components.table_card(
        "📊 Alert Type Rankings",
        alert_rankings
    )


st.write("")
st.write("")


# =====================================================
# ALERT PRODUCT IMPACT
# =====================================================

product_alerts = (
    alerts.groupby("Product")
    .size()
    .reset_index(name="alert_count")
    .sort_values(
        "alert_count",
        ascending=False
    )
)


ui_components.table_card(
    "📦 Product Impact Summary",
    product_alerts
)


st.write("")
st.write("")


# =====================================================
# EXECUTIVE ALERT BRIEF
# =====================================================

multi_alert_products = (
    product_alerts["alert_count"]
    > 1
).sum()

ui_components.ai_brief_panel([
    f"There are currently {total_alerts} active alerts requiring leadership attention.",
    f"{unique_alert_types} different alert categories are being monitored in real time.",
    f"{most_common_alert} is currently the dominant market signal.",
    f"{products_impacted} products are impacted by at least one market signal.",
    f"{multi_alert_products} products are affected by multiple alerts simultaneously.",
    "Products associated with repeated alerts should be escalated for immediate investigation.",
    "Use alert trends to proactively mitigate risk and allocate operational resources."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Complete Alert Feed"
):

    st.dataframe(
        alerts,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Alert Type Summary"
):

    st.dataframe(
        alert_rankings,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Product Alert Summary"
):

    st.dataframe(
        product_alerts,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Market Alert Center continuously monitors market signals and escalates critical events to help executives respond proactively to emerging risks and opportunities."
)