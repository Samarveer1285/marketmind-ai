from datetime import datetime, timezone

import streamlit as st

from providers import get_provider

# Automated ingestion runs twice weekly (Monday & Thursday) -- see
# .github/workflows/refresh_data.yml. The longest gap on schedule is 4 days
# (Thu -> Mon), so that's "on time"; beyond that the badge starts warning
# that a scheduled run was likely missed.
FRESHNESS_OK_HOURS = 4 * 24
FRESHNESS_WARN_HOURS = 8 * 24


@st.cache_data(ttl=300, show_spinner=False)
def _cached_last_refreshed():
    """Cached for 5 minutes so every page load doesn't re-query Supabase --
    this is called from apply_theme(), i.e. once per page per rerun."""
    return get_provider().get_last_refreshed()


def render_freshness_badge():
    """
    "Data last refreshed" indicator, shown in the sidebar on every page (see
    theme.py's apply_theme(), which calls this). Pulled from the real
    provider, not hardcoded -- if the automation stops running, this
    genuinely goes stale/red instead of silently claiming to be live.
    """
    try:
        last_refreshed = _cached_last_refreshed()
    except Exception as e:
        st.sidebar.caption(f"⚪ Data freshness unknown ({e})")
        return

    if last_refreshed is None:
        st.sidebar.caption("⚪ No data ingested yet")
        return

    if last_refreshed.tzinfo is None:
        last_refreshed = last_refreshed.replace(tzinfo=timezone.utc)

    age_hours = (datetime.now(timezone.utc) - last_refreshed).total_seconds() / 3600

    if age_hours <= FRESHNESS_OK_HOURS:
        dot = "🟢"
    elif age_hours <= FRESHNESS_WARN_HOURS:
        dot = "🟡"
    else:
        dot = "🔴"

    age_label = (
        f"{age_hours / 24:.1f} days ago" if age_hours >= 24
        else f"{age_hours:.1f} hours ago"
    )

    st.sidebar.caption(
        f"{dot} Data last refreshed: "
        f"{last_refreshed.strftime('%Y-%m-%d %H:%M UTC')} ({age_label})"
    )


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