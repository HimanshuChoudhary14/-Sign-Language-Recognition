from ui.history import init_db                            # moved here to ensure DB is initialized before any UI or detection logic runs
init_db()

import streamlit as st                                    # use streamlit for UI (streamlit==1.30.0) 
from streamlit_option_menu import option_menu             # for better sidebar navigation (streamlit-option-menu==0.3.0)
from learning_center.ui import render_learning_center     # import learning center UI



# ===== PAGE CONFIG =====
st.set_page_config(page_title="SIGN LANGUAGE DETECTION SYSTEM", layout="wide")

# ===== SESSION DEFAULTS =====
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

if "run" not in st.session_state:
    st.session_state.run = False

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

if "voice_speed" not in st.session_state:
    st.session_state.voice_speed = 150


# ===== UI IMPORTS =====
from ui.styles import load_css, render_header
from ui.dashboard import render_dashboard
from ui.voice_settings import render_voice
from ui.feedback import render_feedback
from ui.history import render_history   # ⭐ add
from ui.about import render_about

# ===== MODULE IMPORTS =====
from modules.detection import run_detection

# ===== LOAD CSS + HEADER =====
load_css()
render_header()

# ===== SIDEBAR =====
with st.sidebar:

    selected = option_menu(
        menu_title="Menu",
        options=[
            "Dashboard",
            "Live Detection",
            "Learning Center",
            "Voice",
            "History & Reports",
            "Feedback",
            "About"
        ],
        icons=["house", "camera-video", "book", "mic", "bar-chart", "chat-dots", "info-circle"],
    )

# ===== ROUTING =====
if selected == "Dashboard":
    render_dashboard()

elif selected == "Live Detection":
    run_detection()

elif selected == "Learning Center":
    render_learning_center()

elif selected == "Voice":
    render_voice()

elif selected == "History & Reports":
    render_history()     # ⭐ add

elif selected == "Feedback":
    render_feedback()

elif selected == "About":
    render_about()

# ===== FOOTER =====
st.markdown("""
<hr>
<p style="text-align:center;color:#64748b;font-size:12px;">
© 2026 Sign Language AI • Built with Streamlit
</p>
""", unsafe_allow_html=True)
