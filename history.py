import sqlite3
import pandas as pd
import streamlit as st
from datetime import date
import plotly.express as px
import json
import os

DB_NAME = "history.db"
DETECTIONS_FILE = "detections.json"


# ================= DB INIT =================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gesture TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_detection(gesture, time):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO detections (gesture, time) VALUES (?, ?)",
        (gesture, time)
    )
    conn.commit()
    conn.close()


def load_history():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM detections", conn)
    conn.close()
    return df


def delete_all_history():
    # ---- clear history.db ----
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM detections")
    conn.commit()
    conn.close()

    # ---- clear Home/Dashboard detections.json ----
    if os.path.exists(DETECTIONS_FILE):
        with open(DETECTIONS_FILE, "w") as f:
            json.dump([], f)


# ================= UI =================
def render_history():

    st.subheader("📜 History & Reports")

    # ---------- GLOBAL CSS ----------
    st.markdown("""
    <style>

    .glass {
        background: linear-gradient(145deg,#020617,#0f172a);
        border:1px solid rgba(148,163,184,0.25);
        border-radius:18px;
        padding:22px;
        backdrop-filter: blur(14px);
        box-shadow:0 0 30px rgba(56,189,248,0.25);
    }

    div[data-baseweb="select"] > div,
    input[type="text"] {
        background:#020617 !important;
        color:#e5e7eb !important;
        border:1px solid rgba(148,163,184,0.3) !important;
        border-radius:12px !important;
    }

    .stDataFrame {
        background:#020617 !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg,#38bdf8,#2563eb) !important;
        color:white !important;
        border-radius:12px !important;
        font-weight:600 !important;
    }

    .delete-btn button {
        background: linear-gradient(135deg,#ef4444,#b91c1c) !important;
        color:white !important;
        border-radius:12px !important;
        font-weight:600 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    df = load_history()

    if not df.empty:
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df["date"] = df["time"].dt.date

    today = date.today()

    # ================= SUMMARY =================
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"<div class='glass'><p>Total Detections</p><h2>{len(df)}</h2></div>",
            unsafe_allow_html=True
        )

    with c2:
        today_count = len(df[df["date"] == today]) if not df.empty else 0
        st.markdown(
            f"<div class='glass'><p>Today's Detections</p><h2>{today_count}</h2></div>",
            unsafe_allow_html=True
        )

    with c3:
        unique_count = df["gesture"].nunique() if not df.empty else 0
        st.markdown(
            f"<div class='glass'><p>✋ Unique Gestures</p><h2>{unique_count}</h2></div>",
            unsafe_allow_html=True
        )

    st.divider()

    # ================= FILTERS =================
    st.subheader("🔍 Filters")

    col1, col2 = st.columns(2)

    with col1:
        sel_gesture = st.selectbox(
            "Filter by Gesture",
            ["All"] + sorted(df["gesture"].unique().tolist()) if not df.empty else ["All"]
        )

    with col2:
        sel_date = st.date_input("Filter by Date", value=None)

    apply = st.button("✅ Apply Filters")

    filtered_df = df.copy()
    if apply and not df.empty:
        if sel_gesture != "All":
            filtered_df = filtered_df[filtered_df["gesture"] == sel_gesture]
        if sel_date:
            filtered_df = filtered_df[filtered_df["date"] == sel_date]

    st.divider()

    # ================= TOP + FREQUENCY =================
    left, right = st.columns(2)

    with left:
        st.subheader("🏆 Top Gestures")
        if filtered_df.empty:
            st.info("No data")
        else:
            top_df = filtered_df["gesture"].value_counts().reset_index()
            top_df.columns = ["Gesture", "Count"]
            st.dataframe(top_df, use_container_width=True, height=400)

    with right:
        st.subheader("📈 Gesture Frequency")
        if filtered_df.empty:
            st.info("No data")
        else:
            freq_df = filtered_df["gesture"].value_counts().reset_index()
            freq_df.columns = ["Gesture", "Count"]

            fig = px.bar(freq_df, x="Gesture", y="Count")
            fig.update_layout(
                height=400,
                plot_bgcolor="white",
                paper_bgcolor="white",
                dragmode=False,
                xaxis=dict(fixedrange=True),
                yaxis=dict(fixedrange=True)
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "scrollZoom": False,
                    "displayModeBar": False,
                    "staticPlot": True
                }
            )

    st.divider()

    # ================= RECENT + FULL =================
    r1, r2 = st.columns(2)

    with r1:
        st.subheader("⏰ Recent Activity (Last 20)")
        if filtered_df.empty:
            st.info("No recent activity")
        else:
            recent_df = filtered_df.sort_values("time", ascending=False).head(20)
            st.dataframe(
                recent_df[["gesture", "time"]],
                use_container_width=True,
                height=350
            )

            # ✅ DOWNLOAD BUTTON MOVED HERE
            csv = filtered_df.drop(columns=["date"]).to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download CSV", csv, "history.csv", "text/csv")

    with r2:
        st.subheader("📋 Full / Filtered History")

        if filtered_df.empty:
            st.info("No history")
        else:
            clean_df = filtered_df.drop(columns=["date"])
            st.dataframe(clean_df, use_container_width=True, height=350)

            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False

            if not st.session_state.confirm_delete:
                if st.button("🗑 Delete All History"):
                    st.session_state.confirm_delete = True
            else:
                st.warning("⚠ This will delete ALL history permanently.")
                confirm = st.checkbox("I understand, delete everything")

                if confirm:
                    st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
                    if st.button("❌ Confirm Delete"):
                        delete_all_history()
                        st.session_state.confirm_delete = False
                        st.success("All history deleted.")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
