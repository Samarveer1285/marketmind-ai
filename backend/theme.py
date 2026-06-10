import streamlit as st
import plotly.io as pio


def apply_theme():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left,
                rgba(108,92,231,0.12),
                transparent 30%),

            radial-gradient(circle at top right,
                rgba(0,194,255,0.10),
                transparent 25%),

            #0B0F19;

        color: #F8FAFC;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #242938;
    }

    h1,h2,h3 {
        color: #F8FAFC;
        font-weight: 700;
    }

    p,label,span {
        color: #94A3B8;
    }

    div[data-testid="stMetric"] {
        background: #0D1816;
        border: 1px solid #1F2D29;
        border-radius: 24px;
        padding: 20px 24px;
        min-height: 140px;

        box-shadow:
            0 8px 30px rgba(0,0,0,0.35);

        transition: all 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);

        border-color: #8EF2C2;

        box-shadow:
            0 0 20px rgba(142,242,194,0.12);
    }  

    div[data-testid="stMetricLabel"] {
        color: #A8B5B0;
        font-size: 15px;
    }

    div[data-testid="stMetricValue"] {
        color: #F5F7F6;
        font-size: 36px;
        font-weight: 700;
    }

    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
    }

    </style>
    """, unsafe_allow_html=True)

    pio.templates.default = "plotly_dark"