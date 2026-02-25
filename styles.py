import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* ---------- REMOVE STREAMLIT DEFAULT TOP BAR ---------- */
    header {visibility: hidden;}

    /* ---------- REMOVE EXTRA TOP SPACE ---------- */
    .block-container {
        padding-top: 0rem !important;
    }

    /* ⭐ BACKGROUND */
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(56,189,248,0.12), transparent 25%),
            radial-gradient(circle at 85% 40%, rgba(96,165,250,0.12), transparent 25%),
            radial-gradient(circle at 50% 90%, rgba(37,99,235,0.10), transparent 30%),
            linear-gradient(180deg,#0f172a,#020617);
        color: white;
    }

     /* ================= OPTION MENU CARD FIX ================= */

/* White card background remove */
section[data-testid="stSidebar"] .css-1d391kg,
section[data-testid="stSidebar"] .css-6qob1r {
    background: linear-gradient(145deg,#1e293b,#0f172a) !important;
    border-radius: 16px !important;
    padding: 18px !important;
    border: 1px solid rgba(96,165,250,0.3) !important;
    box-shadow: 0 0 20px rgba(96,165,250,0.15) !important;
}

/* Menu title "Menu" */
section[data-testid="stSidebar"] h3 {
    font-size: 18px !important;
    font-weight: 600 !important;
    color: #7dd3fc !important;
}

/* Menu text style */
section[data-testid="stSidebar"] .nav-link {
    font-size: 15px !important;
    font-weight: 500 !important;
    color: #cbd5f5 !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    padding: 8px 12px !important;
    transition: 0.3s;
}

/* Hover effect */
section[data-testid="stSidebar"] .nav-link:hover {
    background: rgba(96,165,250,0.15) !important;
    color: #ffffff !important;
}

/* Active menu */
section[data-testid="stSidebar"] .nav-link.active {
    background: linear-gradient(90deg,#2563eb,#3b82f6) !important;
    color: white !important;
    box-shadow: 0 0 14px rgba(59,130,246,0.5) !important;
}

                
    /* ================= BUTTON ================= */

    .stButton>button {
        background: linear-gradient(90deg,#2563eb,#60a5fa) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-weight: 600;
        border: none !important;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.06);
        box-shadow: 0 0 18px rgba(96,165,250,0.7);
    }

    /* ================= METRIC TEXT FIX ================= */

    label, .stMetric label {
        color: #94a3b8 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    .stMetric-value {
        color: #ffffff !important;
        font-size: 34px !important;
        font-weight: 700 !important;
    }

    /* ================= GLOBAL TEXT FIX ================= */

    p, span, label {
        opacity: 1 !important;
        color: #e2e8f0 !important;
    }

    /* ================= HEADER ================= */

    .header-glow::after {
        content: "";
        display: block;
        height: 2px;
        margin-top: 10px;
        background: linear-gradient(90deg, transparent, #38bdf8, transparent);
        box-shadow: 0 0 12px #38bdf8;
    }

    /* ================= SENTENCE BOX ================= */

    .sentence-box {
        background: linear-gradient(145deg,#1e293b,#020617);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(96,165,250,0.3);
        box-shadow: 0 0 20px rgba(96,165,250,0.15);
        font-size: 18px;
        color: #e2e8f0;
    }

    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown(
        """
        <div class="header-glow" style="
            background:#0b1a33;
            padding:24px;
            text-align:center;
            border-bottom:1px solid rgba(96,165,250,0.2);
        ">
            <h1 style="
                margin:0;
                color:#7dd3fc;
                font-weight:700;
                font-size:38px;
                letter-spacing:1px;
            ">
                🤟 Sign Language AI
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
