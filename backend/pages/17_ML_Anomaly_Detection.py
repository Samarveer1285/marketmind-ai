import streamlit as st
import plotly.express as px

from anomaly_detection_ml import *

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ML Anomaly Detection",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

anomalies = detect_ml_anomalies()


# =====================================================
# PREP DATA
# =====================================================

anomalies = anomalies.copy()

anomalies["status"] = anomalies["anomaly"].map(
    {
        -1: "Anomaly",
        1: "Normal"
    }
)


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🤖 ML Anomaly Detection",
    "Use machine learning to surface hidden product irregularities."
)


# =====================================================
# TOP INSIGHTS
# =====================================================

total_products = len(
    anomalies
)

total_anomalies = (
    anomalies["status"] == "Anomaly"
).sum()

normal_products = (
    anomalies["status"] == "Normal"
).sum()

anomaly_rate = round(
    (
        total_anomalies
        /
        total_products
    ) * 100,
    1
) if total_products > 0 else 0


# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:

    ui_components.executive_card(
        "📦",
        "Products Analysed",
        total_products,
        "ML surveillance coverage"
    )


with col2:

    ui_components.executive_card(
        "🚨",
        "ML Anomalies",
        total_anomalies,
        "Flagged products"
    )


with col3:

    ui_components.executive_card(
        "✅",
        "Normal Products",
        normal_products,
        "Within expected behaviour"
    )


with col4:

    ui_components.executive_card(
        "📊",
        "Anomaly Rate",
        f"{anomaly_rate}%",
        "Detection frequency"
    )


st.write("")
st.write("")


# =====================================================
# DETECTION DISTRIBUTION
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    distribution_chart = px.pie(
        anomalies,
        names="status",
        hole=0.65,
        color="status",
        color_discrete_map={
            "Anomaly": "#EF4444",
            "Normal": "#8EF2C2"
        }
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
        "📊 Detection Distribution",
        distribution_chart
    )


with right:

    scatter_data = anomalies.copy()

    scatter_data["price"] = (
        scatter_data["price"]
        .fillna(
            scatter_data["price"].median()
        )
    )

    scatter_data["rating"] = (
        scatter_data["rating"]
        .fillna(3)
    )

    scatter_data["review_count"] = (
        scatter_data["review_count"]
        .fillna(0)
    )

    surveillance_matrix = px.scatter(
        scatter_data,
            x="price",
            y="review_count",
            color="status",
            size="rating",
            hover_name="name",
            color_discrete_map={
                "Anomaly": "#EF4444",
                "Normal": "#8EF2C2"
            }
        )

    surveillance_matrix.update_layout(
        title=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title="Price",
        yaxis_title="Review Count"
    )

    ui_components.chart_card(
        "🎯 Product Surveillance Matrix",
        surveillance_matrix
    )


st.write("")
st.write("")
# =====================================================
# ML ANOMALY RANKINGS
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    anomaly_products = (
        anomalies[
            anomalies["status"] == "Anomaly"
        ]
        .sort_values(
            "review_count",
            ascending=False
        )
    )

    if anomaly_products.empty:
        anomaly_products = pd.DataFrame(
            columns=[
                "name",
                "price",
                "rating",
                "review_count"
            ]
        )

    ui_components.table_card(
        "🚨 ML Detected Anomalies",
        anomaly_products[
            [
                "name",
                "price",
                "rating",
                "review_count"
            ]
        ]
    )


with right:

    normal_products_df = (
        anomalies[
            anomalies["status"] == "Normal"
        ]
        .sort_values(
            "review_count",
            ascending=False
        )
        .head(15)
    )

    ui_components.table_card(
        "✅ Reference Products",
        normal_products_df[
            [
                "name",
                "price",
                "rating",
                "review_count"
            ]
        ]
    )


st.write("")
st.write("")


# =====================================================
# ANOMALY VS NORMAL PROFILES
# =====================================================

profile_summary = (
    anomalies
    .groupby("status")
    .agg({
        "price": "mean",
        "rating": "mean",
        "review_count": "mean"
    })
    .reset_index()
)

profile_summary["price"] = (
    profile_summary["price"]
    .round(2)
)

profile_summary["rating"] = (
    profile_summary["rating"]
    .round(2)
)

profile_summary["review_count"] = (
    profile_summary["review_count"]
    .round(0)
)


ui_components.table_card(
    "📊 Behavioural Profiles",
    profile_summary
)


st.write("")
st.write("")


# =====================================================
# EXECUTIVE ML BRIEF
# =====================================================

if total_anomalies > 0:

    top_anomaly = (
        anomaly_products
        .iloc[0]
    )

    anomaly_message = (
        f"{top_anomaly['name']} is the most commercially significant anomaly based on customer activity."
    )

else:

    anomaly_message = (
        "No meaningful anomalies were identified by the ML model."
    )


high_rating_anomalies = (
    anomaly_products["rating"] > 4
).sum() if total_anomalies > 0 else 0


ui_components.ai_brief_panel([
    f"The ML engine identified {total_anomalies} anomalous products out of {total_products} products analysed.",
    anomaly_message,
    f"{high_rating_anomalies} anomalous products maintain ratings above 4.0, suggesting potentially overlooked opportunities.",
    f"The anomaly rate currently stands at {anomaly_rate}%.",
    "Machine learning surveillance can uncover unusual market behaviour missed by rule-based systems.",
    "Review flagged products regularly to distinguish emerging opportunities from operational risks."
])


st.write("")
st.write("")


# =====================================================
# EXPANDABLE DATASETS
# =====================================================

with st.expander(
    "📋 View Complete ML Detection Dataset"
):

    st.dataframe(
        anomalies,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Only Anomalous Products"
):

    st.dataframe(
        anomaly_products,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "📋 View Normal Products"
):

    st.dataframe(
        anomalies[
            anomalies["status"] == "Normal"
        ],
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "ML Anomaly Detection applies machine learning surveillance to identify unusual product behaviour, enabling early intervention and proactive decision-making."
)