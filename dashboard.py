import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import date

from modules.voice_engine import stop_voice

# ================== DATA PERSISTENCE ==================
DATA_FILE = "detections.json"

def load_detections():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []
# =====================================================


def render_dashboard():

    if not st.session_state.get("run", False):
        stop_voice()

    detections = load_detections()

    if "sentence" not in st.session_state:
        st.session_state["sentence"] = ""

    sentence = st.session_state.get("sentence", "")

    total_predictions = len(detections)

    avg_conf = (
        sum(d["confidence"] for d in detections) / total_predictions
        if total_predictions > 0 else 0
    )

    today = date.today()
    today_detections = []

    for d in detections:
        if "time" in d:
            try:
                if pd.to_datetime(d["time"]).date() == today:
                    today_detections.append(d)
            except:
                pass

    today_count = len(today_detections)

    st.subheader("📊 System Overview")

    c1, c2, c3 = st.columns(3)

    card_style = """
        position: relative;
        background: linear-gradient(145deg,#0f172a,#020617);
        backdrop-filter: blur(16px);
        padding:34px;
        border-radius:22px;
        text-align:center;
        border:1px solid rgba(148,163,184,0.35);
        box-shadow:0 25px 55px rgba(2,6,23,0.95);
    """

    with c1:
        st.markdown(f"""
        <div style="{card_style}">
            <p style="color:#cbd5f5;">Total Predictions</p>
            <h2 style="color:white;">{total_predictions}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="{card_style}">
            <p style="color:#cbd5f5;">Average Confidence</p>
            <h2 style="color:white;">{avg_conf:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="{card_style}">
            <p style="color:#cbd5f5;">Today's Detections</p>
            <h2 style="color:white;">{today_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    # ================== ALWAYS CREATE DF ==================
    df = pd.DataFrame(detections)

    if df.empty:
        st.warning("No detection data available yet.")
    else:

        def decision(conf):
            if conf < 85:
                return "Rejected ❌"
            elif conf < 95:
                return "Suggested 🟡"
            return "Accepted ✅"

        df["decision"] = df["confidence"].apply(decision)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Gesture Distribution")
            gesture_count = df["gesture"].value_counts().reset_index()
            gesture_count.columns = ["Gesture", "Count"]

            fig_bar = px.bar(
                gesture_count,
                x="Gesture",
                y="Count",
                color="Gesture",
                template="plotly_dark"
            )

            fig_bar.update_layout(
                plot_bgcolor="#0f172a",
                paper_bgcolor="#0f172a",
                showlegend=False
            )

            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("⏱ Gesture Detection Frequency Over Time")

            df["time"] = pd.to_datetime(df["time"], errors="coerce")
            timeline = df.groupby("time").size().reset_index(name="Count")

            if timeline.empty:
                st.info("Not enough time data.")
            else:
                fig_time = px.line(
                    timeline,
                    x="time",
                    y="Count",
                    markers=True,
                    template="plotly_dark"
                )

                fig_time.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a"
                )

                st.plotly_chart(fig_time, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("🎯 Confidence Score by Gesture")

            conf_df = (
                df.groupby("gesture")["confidence"]
                .mean()
                .reset_index()
                .sort_values("confidence", ascending=True)
            )

            if conf_df.empty:
                st.info("Not enough data for confidence chart.")
            else:
                fig_conf = px.bar(
                    conf_df,
                    x="confidence",
                    y="gesture",
                    orientation="h",
                    text=conf_df["confidence"].round(2).astype(str) + "%",
                    color="confidence",
                    color_continuous_scale=["#ef4444", "#facc15", "#22c55e"],
                    template="plotly_dark"
                )

                fig_conf.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a",
                    coloraxis_showscale=False
                )

                fig_conf.update_traces(textposition="outside")
                st.plotly_chart(fig_conf, use_container_width=True)

        with col4:
            st.subheader("🔥 Real-Time Gesture Activity (Heatmap)")

            recent_df = df.tail(60).copy()
            recent_df["t"] = range(len(recent_df))

            heatmap_df = (
                recent_df.groupby(["gesture", "t"])
                .size()
                .reset_index(name="count")
            )

            if heatmap_df.empty:
                st.info("Not enough data for heatmap.")
            else:
                fig_heat = px.density_heatmap(
                    heatmap_df,
                    x="t",
                    y="gesture",
                    z="count",
                    color_continuous_scale="Turbo",
                    template="plotly_dark"
                )

                fig_heat.update_layout(
                    plot_bgcolor="#0f172a",
                    paper_bgcolor="#0f172a"
                )

                st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("📝 Detected Sentence")
    st.markdown(f"""
    <div style="
        background:#020617;
        padding:22px;
        border-radius:18px;
        color:#e2e8f0;
        border:1px solid rgba(96,165,250,0.3);
    ">
        {sentence if sentence else "No sentence detected yet..."}
    </div>
    """, unsafe_allow_html=True)