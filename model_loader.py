import pickle
import os
from tensorflow.keras.models import load_model
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_all_models():

    # modules folder path
    current_dir = os.path.dirname(__file__)

    # app folder path
    app_dir = os.path.abspath(os.path.join(current_dir, ".."))

    # Model folder path
    model_path = os.path.join(app_dir, "Model", "gesture_model_one_hand.h5")
    encoder_path = os.path.join(app_dir, "Model", "label_encoder_one_hand.pkl")
    scaler_path = os.path.join(app_dir, "Model", "scaler_one_hand.pkl")

    # 🔥 Safe loading (no debug print, no open leak)
    if not os.path.exists(model_path):
        st.error("Model file not found!")
        return None, None, None

    model = load_model(model_path)

    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)

    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    return model, encoder, scaler