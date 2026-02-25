import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from datetime import datetime
import json
import os

from ui.history import add_detection
from modules.model_loader import load_all_models
from modules.voice_engine import speak          # ✅ ORIGINAL SPEAK
from modules.database import init_db, save_detection


# ================== PERSISTENCE ==================
DATA_FILE = "detections.json"

def save_detections(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_detections():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []
# =================================================

model, encoder, scaler = load_all_models()

CONF_THRESHOLD = 85
SIGN_COOLDOWN = 1.2


def run_detection():

    st.subheader("📹 Live Detection")
    init_db()

    # ================= SESSION STATE =================
    defaults = {
        "run": False,
        "live_detections": [],
        "sentence": "",
        "last_score": 0,
        "last_spoken_sentence": "",
        "last_spoken_gesture": "",
        "last_saved": None,
        "last_sign": None,
        "last_sign_time": 0,
        "voice_on": True,
        "fps": 0
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ================= TOP CONTROLS =================
    colA, colB, colC = st.columns([1,1,1])

    with colA:
        if st.button("▶ Start Camera"):
            st.session_state.run = True
            st.session_state.live_detections = []
            st.session_state.sentence = ""
            st.session_state.last_score = 0
            st.session_state.last_sign = None
            st.session_state.last_sign_time = 0

    with colB:
        if st.button("⏹ Stop Camera"):
            st.session_state.run = False

    with colC:
        st.session_state.voice_on = st.toggle("🔊 Voice Output", value=True)

    # ================= LAYOUT =================
    col1, col2 = st.columns([3, 1])

    frame_window = col1.empty()

    detected_card = col2.empty()
    conf_bar = col2.empty()
    history_box = col2.empty()
    sys_box = col2.empty()

    # ================= MEDIAPIPE =================
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )

    # ================= CAMERA LOOP =================
    if st.session_state.run:

        cap = cv2.VideoCapture(0)
        prev_time = 0

        while st.session_state.run:

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            current_time = time.time()
            st.session_state.fps = int(1 / (current_time - prev_time)) if prev_time else 0
            prev_time = current_time

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            gesture = None
            conf = 0

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    lm_list = []
                    for lm in hand_landmarks.landmark:
                        lm_list.extend([lm.x, lm.y, lm.z])

                    data = scaler.transform([lm_list])
                    pred = model.predict(data)

                    gesture = encoder.inverse_transform(
                        [np.argmax(pred)]
                    )[0]

                    conf = float(np.max(pred) * 100)

            # ================= VOICE + SENTENCE =================
            if gesture and conf >= CONF_THRESHOLD:

                st.session_state.last_score = int(conf)

                if (
                    gesture != st.session_state.last_sign
                    or current_time - st.session_state.last_sign_time > SIGN_COOLDOWN
                ):

                    st.session_state.last_sign = gesture
                    st.session_state.last_sign_time = current_time

                    if st.session_state.voice_on:
                        if gesture != st.session_state.last_spoken_gesture:
                            speak(gesture)
                            st.session_state.last_spoken_gesture = gesture

                    st.session_state.sentence += " " + gesture

                    if st.session_state.voice_on:
                        if st.session_state.sentence != st.session_state.last_spoken_sentence:
                            speak(st.session_state.sentence)
                            st.session_state.last_spoken_sentence = st.session_state.sentence

                    time_label = time.strftime("%H:%M:%S")

                    st.session_state.live_detections.append({
                        "gesture": gesture,
                        "confidence": round(conf, 2),
                        "time": time_label
                    })

                    all_data = load_detections()
                    all_data.append({
                        "gesture": gesture,
                        "confidence": round(conf, 2),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    save_detections(all_data)

                    save_detection(gesture, round(conf, 2), time_label)

                    if st.session_state.last_saved != gesture:
                        add_detection(
                            gesture,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        st.session_state.last_saved = gesture

            # ================= LEFT =================
            frame_window.image(frame, channels="BGR")

            # ================= RIGHT =================
            with detected_card.container():
                st.markdown("### 🤖 Detected Sign")
                if gesture:
                    st.markdown(f"""
                    <div style="background:#0f172a;padding:30px;border-radius:15px;
                    text-align:center;font-size:48px;font-weight:bold;color:#22c55e;">
                        {gesture}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Waiting for hand...")

            with conf_bar.container():
                st.markdown("### 🎯 Confidence")
                st.progress(min(int(conf), 100))
                st.caption(f"{conf:.2f} %")

            with history_box.container():
                st.markdown("### 🕒 Recent Signs")
                for item in st.session_state.live_detections[-5:][::-1]:
                    st.write(f"• {item['gesture']} — {item['confidence']}%")

            with sys_box.container():
                st.markdown("### ⚙ System Info")
                st.write(f"⚡ FPS: {st.session_state.fps}")
                st.write("🧠 Model: CNN + MediaPipe")

        cap.release()

    # ================= BOTTOM =================
    st.metric("⭐ Last Gesture Accuracy", st.session_state.last_score)

    st.write("### 📝 Sentence Builder")
    st.write(st.session_state.sentence)

    if st.session_state.live_detections:
        st.write("### 📊 Detection History (Current Session)")
        st.dataframe(st.session_state.live_detections)