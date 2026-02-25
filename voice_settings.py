import streamlit as st
from modules.voice_engine import speak
import os
import base64
import streamlit.components.v1 as components


# 🔥 CACHE VIDEO (FIX FOR LOADING)
@st.cache_data(show_spinner=False)
def load_video_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def render_voice():

    # 🔥 Ensure voice flag exists (prevents cross-page glitch)
    st.session_state.setdefault("voice_running", False)

    col1, col2 = st.columns([2, 1])

    # ================= LEFT PANEL =================
    with col1:

        st.subheader("🔊 Voice Settings")

        st.session_state.setdefault("voice_enabled", True)
        st.session_state.setdefault("voice_speed", 150)
        st.session_state.setdefault("voice_language", "English")
        st.session_state.setdefault("voice_gender", "Male")
        st.session_state.setdefault("speaking", False)

        st.markdown("""
        <style>
        div[data-baseweb="select"] > div {
            background:#1e293b !important;
            color:white !important;
        }
        .stTextInput input {
            background:#1e293b !important;
            color:white !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.session_state.voice_enabled = st.toggle(
            "Enable Voice Output",
            value=st.session_state.voice_enabled
        )

        st.session_state.voice_speed = st.slider(
            "Voice Speed",
            100,
            200,
            st.session_state.voice_speed
        )

        st.session_state.voice_language = st.selectbox(
            "Language",
            ["English", "Hindi"]
        )

        st.session_state.voice_gender = st.radio(
            "Gender",
            ["Male", "Female"],
            horizontal=True
        )

        text = st.text_input("Test Voice")

        if st.button("Test"):
            if text:
                st.session_state.speaking = True
                st.session_state.voice_running = True
                speak(text)
                st.session_state.voice_running = False
                st.session_state.speaking = False

    # ================= RIGHT PANEL =================
    with col2:

        st.markdown("### 🤖 AI Voice Assistant")

        # 🔥 Dynamic path (no hardcoded PC path)
        current_dir = os.path.dirname(__file__)
        app_dir = os.path.abspath(os.path.join(current_dir, ".."))
        video_path = os.path.join(app_dir, "assets", "jarvis.mp4")

        st.markdown("""
        <style>
        .jarvis-box {
            background: linear-gradient(145deg,#0f172a,#020617);
            padding:18px;
            border-radius:20px;
            border:1px solid rgba(56,189,248,0.4);
            box-shadow:0 0 20px rgba(56,189,248,0.3);
            margin-bottom:20px;
            text-align:center;
        }
        </style>
        """, unsafe_allow_html=True)

        # ---------- VIDEO (CACHED) ----------
        video_base64 = load_video_base64(video_path)

        if video_base64:
            st.markdown(f"""
            <div class="jarvis-box">
            <video autoplay loop muted width="100%" style="border-radius:15px;">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
            </div>
            """, unsafe_allow_html=True)

        # ================= 🌊 REAL-TIME VOICE WAVEFORM =================
        components.html("""
        <div style="
            margin-top:18px;
            background:#020617;
            border-radius:18px;
            border:1px solid rgba(56,189,248,0.5);
            box-shadow:0 0 30px rgba(56,189,248,0.35);
            padding:14px;
        ">
            <div style="
                color:#38bdf8;
                font-size:14px;
                font-weight:600;
                text-align:center;
                margin-bottom:10px;
            ">
                Live Voice Frequency
            </div>

            <canvas id="wave" width="320" height="90"></canvas>
        </div>

        <script>
        const canvas = document.getElementById("wave");
        const ctx = canvas.getContext("2d");

        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const analyser = audioCtx.createAnalyser();
            const source = audioCtx.createMediaStreamSource(stream);
            source.connect(analyser);
            analyser.fftSize = 2048;

            const bufferLength = analyser.fftSize;
            const dataArray = new Uint8Array(bufferLength);

            function draw() {
                requestAnimationFrame(draw);
                analyser.getByteTimeDomainData(dataArray);

                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.beginPath();
                ctx.lineWidth = 3;
                ctx.strokeStyle = "rgba(56,189,248,0.9)";

                let sliceWidth = canvas.width / bufferLength;
                let x = 0;

                for (let i = 0; i < bufferLength; i++) {
                    let v = dataArray[i] / 128.0;
                    let y = v * canvas.height / 2;

                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);

                    x += sliceWidth;
                }

                ctx.stroke();
            }

            draw();
        });
        </script>
        """, height=210)
