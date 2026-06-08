import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from analytics_function import *

st.set_page_config(layout="wide")

st.title("💰 Pricing Analytics")

overpriced = get_overpriced_products()
undervalued = get_undervalued_products()
drops = get_biggest_price_drops()

st.subheader("🚨 Overpriced Products")
st.dataframe(overpriced)

st.subheader("💎 Undervalued Products")
st.dataframe(undervalued)

st.subheader("📉 Biggest Price Drops")
st.dataframe(drops)