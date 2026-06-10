import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from analytics_function import *
import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Pricing Analytics",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD DATA
# =====================================================

overpriced = get_overpriced_products()

undervalued = get_undervalued_products()

drops = get_biggest_price_drops()


# =====================================================
# PAGE HEADER
# =====================================================

ui_components.page_header(
    "💰 Pricing Analytics",
    "Monitor pricing inefficiencies and identify value opportunities."
)


# =====================================================
# KPI SECTION
# =====================================================

most_expensive = overpriced.iloc[0]

best_value = undervalued.iloc[0]

largest_drop = drops.iloc[0]

avg_overpriced = round(
    overpriced["price"].mean(),
    0
)

col1, col2, col3, col4 = st.columns(
    4,
    gap="large"
)

with col1:
    ui_components.executive_card(
        "🚨",
        "Overpriced",
        len(overpriced),
        "Products to monitor"
    )

with col2:
    ui_components.executive_card(
        "💎",
        "Best Value",
        best_value["name"],
        f"Score: {best_value['value_score']:.1f}"
    )

with col3:
    ui_components.executive_card(
        "📉",
        "Largest Drop",
        f"{largest_drop['price_change_pct']:.0f}%",
        largest_drop["name"]
    )

with col4:
    ui_components.executive_card(
        "💰",
        "Avg Price",
        f"₹{avg_overpriced:,.0f}",
        "Overpriced basket"
    )


st.write("")
st.write("")


# =====================================================
# OVERPRICED + PRICE DROPS
# =====================================================

left, right = st.columns(
    [2, 1],
    gap="large"
)

with left:

    price_chart = px.bar(
        overpriced.head(10).sort_values(
            "price",
            ascending=True
        ),
        x="price",
        y="name",
        orientation="h",
        color="price",
        color_continuous_scale=[
            "#FF6B6B",
            "#F97316"
        ]
    )

    price_chart.update_layout(
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
        xaxis_title="Price",
        yaxis_title=""
    )

    ui_components.chart_card(
        "🚨 Overpriced Watchlist",
        price_chart
    )


with right:

    drop_chart = px.bar(
        drops.head(8).sort_values(
            "price_change_pct",
            ascending=True
        ),
        x="price_change_pct",
        y="name",
        orientation="h",
        color="price_change_pct",
        color_continuous_scale=[
            "#5AD7D1",
            "#8EF2C2"
        ]
    )

    drop_chart.update_layout(
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
        xaxis_title="% Drop",
        yaxis_title=""
    )

    ui_components.chart_card(
        "📉 Biggest Price Drops",
        drop_chart
    )


st.write("")
st.write("")
# =====================================================
# VALUE OPPORTUNITY EXPLORER
# =====================================================

value_scatter = px.scatter(
    undervalued.head(30),
    x="price",
    y="rating",
    size="value_score",
    color="value_score",
    hover_name="name",
    color_continuous_scale=[
        "#5AD7D1",
        "#8EF2C2"
    ]
)

value_scatter.update_layout(
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
    xaxis_title="Price",
    yaxis_title="Rating"
)

ui_components.chart_card(
    "💎 Value Opportunity Explorer",
    value_scatter
)


st.write("")
st.write("")


# =====================================================
# TABLES
# =====================================================

left, right = st.columns(
    2,
    gap="large"
)

with left:

    best_value_table = undervalued[
        [
            "name",
            "price",
            "rating",
            "value_score"
        ]
    ].head(10)

    ui_components.table_card(
        "💎 Best Value Products",
        best_value_table
    )


with right:

    overpriced_table = overpriced[
        [
            "name",
            "price"
        ]
    ].head(10)

    ui_components.table_card(
        "🚨 Overpriced Products",
        overpriced_table
    )


st.write("")
st.write("")


# =====================================================
# EXECUTIVE PRICING BRIEF
# =====================================================

ui_components.ai_brief_panel([
    f"{len(overpriced)} products appear significantly overpriced.",
    f"{best_value['name']} currently offers the strongest value proposition.",
    f"{largest_drop['name']} experienced the biggest price decline ({largest_drop['price_change_pct']:.0f}%).",
    "Price inefficiencies indicate opportunities for portfolio optimization."
])


# =====================================================
# RAW DATA EXPANDERS
# =====================================================

with st.expander("📋 View Full Overpriced Dataset"):

    st.dataframe(
        overpriced,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Undervalued Dataset"):

    st.dataframe(
        undervalued,
        use_container_width=True,
        hide_index=True
    )


with st.expander("📋 View Full Price Drops Dataset"):

    st.dataframe(
        drops,
        use_container_width=True,
        hide_index=True
    )