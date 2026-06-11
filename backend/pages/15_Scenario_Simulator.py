import streamlit as st
import plotly.express as px
import pandas as pd

from load_products import get_latest_market_data
from scenario_simulator import (
    simulate_price_change,
    simulate_rating_improvement,
    simulate_review_growth
)

import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Scenario Simulator",
    layout="wide"
)

apply_theme()


# =====================================================
# LOAD PRODUCTS
# =====================================================

live_data = get_latest_market_data()

if live_data.empty:
    st.warning("No live simulation data available.")
    st.stop()

products = sorted(
    live_data["title"].unique()
)
# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🎯 Scenario Simulator",
    "Test strategic decisions before the market reacts."
)


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "💰 Price Simulation",
    "⭐ Rating Simulation",
    "📈 Marketing Simulation"
])


# =====================================================
# PRICE SIMULATION
# =====================================================

with tab1:

    st.subheader(
        "💰 Price Change Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="price_product"
    )

    price_change = st.slider(
        "Price Change %",
        -50,
        50,
        0
    )

    if st.button(
        "Run Price Simulation"
    ):

        result = simulate_price_change(
            selected_product,
            price_change
        )

        row = result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            ui_components.executive_card(
                "💵",
                "Current Price",
                f"₹{row['current_price']:,.0f}",
                "Existing pricing"
            )

        with col2:

            ui_components.executive_card(
                "🆕",
                "Projected Price",
                f"₹{row['new_price']:,.0f}",
                f"{price_change:+.0f}% adjustment"
            )

        with col3:

            ui_components.executive_card(
                "🛒",
                "Current Reviews",
                int(row["current_reviews"]),
                "Current demand"
            )

        with col4:

            ui_components.executive_card(
                "📈",
                "Projected Reviews",
                int(row["projected_reviews"]),
                f"{row['demand_change_pct']:+.1f}% demand"
            )

        st.write("")
        st.write("")

        comparison = pd.DataFrame({
            "Metric": [
                "Price",
                "Reviews"
            ],
            "Current": [
                row["current_price"],
                row["current_reviews"]
            ],
            "Projected": [
                row["new_price"],
                row["projected_reviews"]
            ]
        })

        fig = px.bar(
            comparison.melt(
                id_vars="Metric",
                var_name="Scenario",
                value_name="Value"
            ),
            x="Metric",
            y="Value",
            color="Scenario",
            barmode="group"
        )

        fig.update_layout(
            title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        ui_components.chart_card(
            "📊 Price Impact Analysis",
            fig
        )

        if row["demand_change_pct"] > 0:

            st.success(
                f"Reducing price by {abs(price_change)}% is projected to improve demand by {row['demand_change_pct']:.1f}%."
            )

        elif row["demand_change_pct"] < 0:

            st.warning(
                f"The proposed pricing change may reduce demand by {abs(row['demand_change_pct']):.1f}%."
            )

        else:

            st.info(
                "The selected scenario is expected to have minimal impact on demand."
            )

        with st.expander(
            "📋 View Simulation Output"
        ):

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )
# =====================================================
# RATING SIMULATION
# =====================================================

with tab2:

    st.subheader(
        "⭐ Rating Improvement Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="rating_product"
    )

    new_rating = st.slider(
        "Projected Rating",
        1.0,
        5.0,
        4.5,
        0.1
    )

    if st.button(
        "Run Rating Simulation"
    ):

        result = simulate_rating_improvement(
            selected_product,
            new_rating
        )

        row = result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            ui_components.executive_card(
                "⭐",
                "Current Rating",
                f"{row['current_rating']:.2f}",
                "Customer perception"
            )

        with col2:

            ui_components.executive_card(
                "🌟",
                "Projected Rating",
                f"{row['projected_rating']:.2f}",
                "Target rating"
            )

        with col3:

            ui_components.executive_card(
                "🤝",
                "Current Trust",
                f"{row['current_trust_score']:.1f}",
                "Trust score"
            )

        with col4:

            ui_components.executive_card(
                "📈",
                "Projected Trust",
                f"{row['projected_trust_score']:.1f}",
                f"{row['trust_change_pct']:+.1f}% change"
            )

        st.write("")
        st.write("")

        col_left, col_right = st.columns(
            2,
            gap="large"
        )

        with col_left:

            trust_df = pd.DataFrame({
                "Scenario": [
                    "Current",
                    "Projected"
                ],
                "Trust Score": [
                    row["current_trust_score"],
                    row["projected_trust_score"]
                ]
            })

            trust_chart = px.bar(
                trust_df,
                x="Scenario",
                y="Trust Score",
                color="Scenario"
            )

            trust_chart.update_layout(
                title=None,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            ui_components.chart_card(
                "🤝 Trust Impact",
                trust_chart
            )


        with col_right:

            opp_df = pd.DataFrame({
                "Scenario": [
                    "Current",
                    "Projected"
                ],
                "Opportunity Score": [
                    row["current_opportunity"],
                    row["projected_opportunity"]
                ]
            })

            opp_chart = px.bar(
                opp_df,
                x="Scenario",
                y="Opportunity Score",
                color="Scenario"
            )

            opp_chart.update_layout(
                title=None,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            ui_components.chart_card(
                "💎 Opportunity Uplift",
                opp_chart
            )

        st.write("")
        st.write("")

        if row["trust_change_pct"] > 0:

            st.success(
                f"Improving ratings to {row['projected_rating']:.1f} could increase trust by {row['trust_change_pct']:.1f}% and improve opportunity potential."
            )

        elif row["trust_change_pct"] < 0:

            st.warning(
                f"The projected rating reduces trust by {abs(row['trust_change_pct']):.1f}%."
            )

        else:

            st.info(
                "The proposed rating scenario produces minimal change."
            )

        with st.expander(
            "📋 View Simulation Output"
        ):

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )
# =====================================================
# MARKETING SIMULATION
# =====================================================

with tab3:

    st.subheader(
        "📈 Marketing Growth Impact"
    )

    selected_product = st.selectbox(
        "Select Product",
        products,
        key="marketing_product"
    )

    growth_pct = st.slider(
        "Review Growth %",
        0,
        200,
        20
    )

    if st.button(
        "Run Marketing Simulation"
    ):

        result = simulate_review_growth(
            selected_product,
            growth_pct
        )

        row = result.iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            ui_components.executive_card(
                "🛒",
                "Current Reviews",
                int(row["current_reviews"]),
                "Current demand"
            )

        with col2:

            ui_components.executive_card(
                "🚀",
                "Projected Reviews",
                int(row["projected_reviews"]),
                f"+{growth_pct}% campaign"
            )

        with col3:

            ui_components.executive_card(
                "📊",
                "Current Market Score",
                f"{row['current_market_score']:.1f}",
                "Market standing"
            )

        with col4:

            ui_components.executive_card(
                "🏆",
                "Projected Market",
                f"{row['projected_market_score']:.1f}",
                "Expected standing"
            )

        st.write("")
        st.write("")

        left, right = st.columns(
            2,
            gap="large"
        )

        with left:

            review_df = pd.DataFrame({
                "Scenario": [
                    "Current",
                    "Projected"
                ],
                "Reviews": [
                    row["current_reviews"],
                    row["projected_reviews"]
                ]
            })

            review_chart = px.bar(
                review_df,
                x="Scenario",
                y="Reviews",
                color="Scenario"
            )

            review_chart.update_layout(
                title=None,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            ui_components.chart_card(
                "📈 Demand Growth Impact",
                review_chart
            )


        with right:

            market_df = pd.DataFrame({
                "Scenario": [
                    "Current",
                    "Projected"
                ],
                "Market Score": [
                    row["current_market_score"],
                    row["projected_market_score"]
                ]
            })

            market_chart = px.bar(
                market_df,
                x="Scenario",
                y="Market Score",
                color="Scenario"
            )

            market_chart.update_layout(
                title=None,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            ui_components.chart_card(
                "🏆 Market Position Impact",
                market_chart
            )

        st.write("")
        st.write("")

        trust_df = pd.DataFrame({
            "Scenario": [
                "Current",
                "Projected"
            ],
            "Trust Score": [
                row["current_trust_score"],
                row["projected_trust_score"]
            ]
        })

        trust_chart = px.line(
            trust_df,
            x="Scenario",
            y="Trust Score",
            markers=True
        )

        trust_chart.update_layout(
            title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        ui_components.chart_card(
            "🤝 Trust Evolution",
            trust_chart
        )

        st.write("")
        st.write("")

        market_change = (
            (
                row["projected_market_score"]
                - row["current_market_score"]
            )
            /
            row["current_market_score"]
        ) * 100

        if row["current_trust_score"] != 0:

            trust_change = (
                (
            row["projected_trust_score"]
            - row["current_trust_score"]
                )
                /
                row["current_trust_score"]
            ) * 100

        else:

            trust_change = 0

        ui_components.ai_brief_panel([
            f"A {growth_pct}% increase in reviews is projected to raise total reviews from {int(row['current_reviews'])} to {int(row['projected_reviews'])}.",
            f"Market score is expected to change from {row['current_market_score']:.1f} to {row['projected_market_score']:.1f} ({market_change:+.1f}%).",
            f"Trust score moves from {row['current_trust_score']:.1f} to {row['projected_trust_score']:.1f} ({trust_change:+.1f}%).",
            "Marketing investments appear to improve both visibility and competitive positioning.",
            "Prioritize campaigns where review growth produces the largest market score uplift."
        ])

        with st.expander(
            "📋 View Simulation Output"
        ):

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Scenario Simulator enables leadership teams to test pricing, quality, and marketing decisions before committing resources in the real market."
)