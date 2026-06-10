import streamlit as st


def render_hero():

    st.title("🧿 MarketMind AI")

    st.subheader("Executive Intelligence Platform")

    st.caption("Signal • Predict • Decide")

    st.divider()


def executive_card(icon, title, value, subtitle):

    value = str(value)

    with st.container(border=True):

        top1, top2 = st.columns([9, 1])

        with top1:
            st.caption(f"{icon} {title}")

        with top2:
            st.caption("↗")

        # Dynamic font sizing
        if len(value) <= 10:
            font_size = 38
        elif len(value) <= 18:
            font_size = 30
        else:
            font_size = 24

        st.markdown(
            f"""
            <div style="
                font-size:{font_size}px;
                font-weight:700;
                line-height:1.2;
                min-height:90px;
                display:flex;
                align-items:center;
                overflow-wrap:break-word;
                word-break:break-word;
            ">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(subtitle)


def ai_brief_panel(insights):

    st.subheader("🧠 AI Market Brief")

    for insight in insights:
        st.markdown(f"- {insight}")

    st.divider()


def section_header(icon, title):

    st.markdown(
        f"## {icon} {title}"
    )


def page_header(title, subtitle=""):

    col1, col2 = st.columns([4, 1])

    with col1:

        st.title(title)

        if subtitle:
            st.caption(subtitle)

    with col2:

        st.text_input(
            "",
            placeholder="Search...",
            key=f"search_{title}"
        )

    st.write("")


def chart_card(title, fig):

    with st.container(border=True):

        st.subheader(title)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


def table_card(title, df):

    with st.container(border=True):

        st.subheader(title)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )