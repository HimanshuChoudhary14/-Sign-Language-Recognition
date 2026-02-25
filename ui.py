import streamlit as st
from modules.model_loader import load_all_models
from duckduckgo_search import DDGS   # ⭐ Image search import


# ⭐ Load model
model, encoder, scaler = load_all_models()


# ⭐ Image Fetch Function
def fetch_sign_image(sign_name):

    query = f"{sign_name} sign language hand gesture"

    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))

            if results:
                return results[0]["image"]
            else:
                return None

    except:
        return None


def render_learning_center():

    st.subheader("📘 Learning Center")

    # ⭐ Selectbox colour fix
    st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        background-color:#1e293b !important;
        color:white !important;
        border-radius:10px !important;
        border:1px solid rgba(96,165,250,0.3) !important;
    }

    div[data-baseweb="select"] svg {
        color:white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===============================
    # ⭐ Welcome Card
    # ===============================
    st.markdown("""
    <div style="
        background: linear-gradient(145deg,#1e293b,#020617);
        padding:25px;
        border-radius:18px;
        border:1px solid rgba(96,165,250,0.3);
        box-shadow:0 0 20px rgba(96,165,250,0.15);
    ">
        <h3 style="color:#7dd3fc;">👋 Welcome to Learning Center</h3>
        <p>Here you can:</p>
        <ul>
            <li>Learn basic hand signs</li>
            <li>Practice gestures</li>
            <li>Improve recognition accuracy</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ⭐ Dynamic Signs
    # ===============================
    try:
        signs = sorted(list(encoder.classes_))
    except:
        signs = ["No Signs Found"]

    selected_sign = st.selectbox(
        "Select a Sign to Learn",
        signs,
        key="learning_sign_selector"
    )

    # ===============================
    # ⭐ Gesture Card
    # ===============================
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg,#1e293b,#020617);
        padding:25px;
        border-radius:18px;
        border:1px solid rgba(96,165,250,0.3);
        box-shadow:0 0 20px rgba(96,165,250,0.15);
    ">
        <h3>✋ Sign: {selected_sign}</h3>
        <p>Show this gesture in front of camera in Live Detection mode.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ⭐ Auto Sign Image Preview (SIZE FIXED)
    # ===============================
    image_url = fetch_sign_image(selected_sign)

    if image_url:
        st.markdown("### 📷 Gesture Example")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
              st.image(image_url, width=360)


    else:
        st.warning("Image not found for this sign")

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # ⭐ Practice Tips Card
    # ===============================
    st.markdown("""
    <div style="
        background: linear-gradient(145deg,#022c22,#020617);
        padding:20px;
        border-radius:18px;
        border:1px solid rgba(16,185,129,0.3);
        box-shadow:0 0 20px rgba(16,185,129,0.15);
    ">
        🚀 Practice regularly to improve accuracy
    </div>
    """, unsafe_allow_html=True)
