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

import langchain_agent
import ui_components
from theme import apply_theme


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Analyst Copilot",
    layout="wide"
)

apply_theme()


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# =====================================================
# HEADER
# =====================================================

ui_components.page_header(
    "🤖 AI Analyst Copilot",
    "Your executive market intelligence assistant."
)


# =====================================================
# QUICK PROMPTS
# =====================================================

st.subheader("⚡ Suggested Questions")

p1, p2, p3, p4 = st.columns(4)

with p1:

    if st.button(
        "🚀 Fastest Growth",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "Which products are growing the fastest?"
        )

with p2:

    if st.button(
        "⚠️ Biggest Risks",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "Which products have the highest risk and why?"
        )

with p3:

    if st.button(
        "💎 Opportunities",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "What are the biggest opportunities in the market?"
        )

with p4:

    if st.button(
        "🏆 Recommendations",
        use_container_width=True
    ):
        st.session_state.pending_prompt = (
            "What actions should management prioritize?"
        )


st.write("")
st.write("")


# =====================================================
# CHAT HISTORY
# =====================================================

st.subheader("💬 Conversation")

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =====================================================
# INPUT AREA
# =====================================================

user_prompt = st.chat_input(
    "Ask MarketMind AI..."
)

if st.session_state.pending_prompt:

    user_prompt = (
        st.session_state.pending_prompt
    )

    st.session_state.pending_prompt = None

# =====================================================
# ASSISTANT RESPONSE
# =====================================================

if user_prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(user_prompt)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "MarketMind AI is analyzing the market..."
        ):

            try:

                answer = langchain_agent.ask_agent(
                    user_prompt
                )
            except Exception as e:

                answer = (
                    f"Unable to generate response.\n\n{str(e)}"
                )

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


st.write("")
st.write("")


# =====================================================
# RESET CHAT
# =====================================================

left, right = st.columns([1, 4])

with left:

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.pending_prompt = None

        st.rerun()


with right:

    st.caption(
        "Powered by Gemini • MarketMind Executive Intelligence"
    )


st.write("")
st.write("")


# =====================================================
# EMPTY STATE
# =====================================================

if len(st.session_state.messages) == 0:

    ui_components.ai_brief_panel([
        "Ask about growth trends and emerging opportunities.",
        "Identify products with the highest risk exposure.",
        "Discover which brands are accelerating fastest.",
        "Get executive recommendations backed by market signals."
    ])