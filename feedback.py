import streamlit as st
import time
from modules.database import save_feedback   # ✅ DB SAVE IMPORT


def render_feedback():

    st.subheader("💬 Feedback")

    # ================= 🎨 FULL DARK THEME OVERRIDE =================
    st.markdown("""
    <style>

    /* ---------- Selectbox ---------- */
    div[data-baseweb="select"] > div {
        background-color: #020617 !important;
        color: #e5e7eb !important;
        border-radius: 10px !important;
        border: 1px solid rgba(56,189,248,0.4) !important;
    }

    /* ---------- Text Area ---------- */
    textarea {
        background-color: #020617 !important;
        color: #e5e7eb !important;
        border-radius: 12px !important;
        border: 1px solid rgba(56,189,248,0.4) !important;
    }

    textarea::placeholder {
        color: #94a3b8 !important;
    }

    textarea:focus,
    div[data-baseweb="select"] > div:focus-within {
        box-shadow: 0 0 12px rgba(56,189,248,0.6) !important;
        border-color: #38bdf8 !important;
    }

    /* ================= FIXED SUBMIT BUTTON ================= */

    /* Target correct Streamlit form button */
    button[kind="secondaryFormSubmit"],
    button[kind="secondaryFormSubmit"]:hover,
    button[kind="secondaryFormSubmit"]:active,
    button[kind="secondaryFormSubmit"]:focus,
    button[kind="secondaryFormSubmit"]:focus-visible {

        background: linear-gradient(135deg, #22d3ee, #38bdf8) !important;
        color: #020617 !important;
        border: none !important;
        padding: 0.75em 2em !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 24px rgba(34,211,238,0.6) !important;
        opacity: 1 !important;
        filter: none !important;
        outline: none !important;
    }

    button[kind="secondaryFormSubmit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 36px rgba(34,211,238,0.9) !important;
        background: linear-gradient(135deg, #38bdf8, #22d3ee) !important;
    }

    /* Force override disabled look */
    button[kind="secondaryFormSubmit"]:disabled {
        background: linear-gradient(135deg, #22d3ee, #38bdf8) !important;
        color: #020617 !important;
        opacity: 1 !important;
        cursor: pointer !important;
    }

    /* ---------- Expander ---------- */
    div[data-testid="stExpander"] {
        background: linear-gradient(145deg,#020617,#0f172a) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(56,189,248,0.35) !important;
        box-shadow: 0 0 20px rgba(56,189,248,0.25) !important;
    }

    div[data-testid="stExpander"] summary {
        color: #e5e7eb !important;
        font-weight: 600 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= LOGIC =================
    st.session_state.setdefault("last_feedback_time", 0)

    with st.form("feedback_form", clear_on_submit=True):

        rating = st.radio(
            "⭐ Rate your experience",
            ["😡 Very Bad", "😕 Bad", "😐 Okay", "🙂 Good", "😍 Excellent"],
            horizontal=True
        )

        feedback_type = st.selectbox(
            "Feedback Type",
            ["Suggestion", "Bug Report","Other"]
        )

        text = st.text_area(
            "Write your feedback",
            placeholder="Anything you want to share (even short feedback is okay 🙂)"
        )

        submitted = st.form_submit_button("Submit Feedback")

    if submitted:

        now = time.time()
        if now - st.session_state.last_feedback_time < 2:
            st.info("⏳ Please wait a moment before submitting again.")
            return

        st.session_state.last_feedback_time = now

        feedback_time = time.strftime("%Y-%m-%d %H:%M:%S")

        save_feedback(
            rating=rating,
            feedback_type=feedback_type,
            feedback_text=text,
            time=feedback_time
        )

        st.markdown("""
        <div style="
            background:linear-gradient(145deg,#020617,#0f172a);
            border:1px solid rgba(34,197,94,0.6);
            padding:20px;
            border-radius:16px;
            box-shadow:0 0 28px rgba(34,197,94,0.35);
            color:#dcfce7;
            margin-top:14px;
        ">
            ✅ <b>Feedback submitted successfully!</b><br>
            Thank you for helping us improve.
        </div>
        """, unsafe_allow_html=True)
