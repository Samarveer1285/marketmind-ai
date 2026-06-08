import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import ai_copilot


st.set_page_config(
    layout="wide"
)

st.title("🤖 AI Analyst Copilot")

question = st.text_input(
    "Ask MarketMind AI"
)

if st.button("Ask"):

    answer = (
        ai_copilot.answer_question(
            question
        )
    )

    st.success(answer)