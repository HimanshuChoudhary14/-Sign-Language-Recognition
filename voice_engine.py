import pyttsx3
import threading
import streamlit as st
import time

engine_lock = threading.Lock()

# ---------- SESSION FLAGS (SAME AS YOUR CODE) ----------
st.session_state.setdefault("voice_stop", False)
st.session_state.setdefault("last_spoken_text", "")
st.session_state.setdefault("last_spoken_time", 0)

# ---------- ENGINE INIT ONCE (FIX) ----------
_engine = pyttsx3.init("sapi5")
_engine.setProperty("rate", 150)
_engine.setProperty("volume", 1.0)

voices = _engine.getProperty("voices")
_engine.setProperty("voice", voices[0].id)


def stop_voice():
    """Call when camera stops"""
    st.session_state.voice_stop = True
    st.session_state.last_spoken_text = ""


def resume_voice():
    """Call when camera starts"""
    st.session_state.voice_stop = False


def speak(text):

    if not text:
        return

    # ❌ Voice disabled
    if not st.session_state.get("voice_enabled", True):
        return

    # ❌ Camera stopped
    if st.session_state.voice_stop:
        return

    # ⏱ Cooldown for repeat text (1.5 sec)
    now = time.time()
    if (
        text == st.session_state.last_spoken_text
        and now - st.session_state.last_spoken_time < 1.5
    ):
        return

    def run():
        with engine_lock:
            try:
                if st.session_state.voice_stop:
                    return

                st.session_state.last_spoken_text = text
                st.session_state.last_spoken_time = time.time()

                _engine.say(text)
                _engine.runAndWait()

            except Exception as e:
                print("Voice Error:", e)

    threading.Thread(target=run, daemon=True).start()
