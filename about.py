import streamlit as st

def render_about():

    st.markdown("""
    <style>

    /* ================= GLOBAL ================= */
    body {
        background-color: #020617;
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }

    .container {
        max-width: 1100px;
        margin: auto;
        padding: 20px;
    }

    /* ================= HEADER ================= */
    .hero-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(90deg,#38bdf8,#0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero-sub {
        text-align: center;
        font-size: 17px;
        color: #cbd5e1;
        margin-bottom: 45px;
    }

    /* ================= CARD ================= */
    .card {
        background: linear-gradient(145deg,#0f172a,#020617);
        border-radius: 22px;
        padding: 32px;
        margin-bottom: 30px;
        border: 1px solid rgba(56,189,248,0.25);
        box-shadow: 0 0 35px rgba(56,189,248,0.15);
        transition: 0.3s ease;
    }

    .card:hover {
        box-shadow: 0 0 45px rgba(56,189,248,0.35);
        transform: translateY(-4px);
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #7dd3fc;
        margin-bottom: 15px;
    }

    .text {
        font-size: 16px;
        line-height: 1.85;
        color: #e5e7eb;
    }

    /* ================= DIVIDER LINE ================= */
    .divider {
        height: 1px;
        background: linear-gradient(90deg,transparent,#38bdf8,transparent);
        margin: 35px 0;
    }

    /* ================= STATS ================= */
    .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit,minmax(220px,1fr));
        gap: 20px;
    }

    .stat-box {
        background: linear-gradient(145deg,#020617,#0f172a);
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(56,189,248,0.3);
        box-shadow: 0 0 20px rgba(56,189,248,0.2);
        transition: 0.3s;
    }

    .stat-box:hover {
        transform: scale(1.05);
        box-shadow: 0 0 35px rgba(56,189,248,0.4);
    }

    .stat-num {
        font-size: 32px;
        font-weight: 800;
        color: #38bdf8;
    }

    .stat-label {
        font-size: 14px;
        color: #94a3b8;
    }

    /* ================= CAPABILITIES ================= */
    .cap-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit,minmax(260px,1fr));
        gap: 20px;
    }

    .cap-box {
        background: linear-gradient(145deg,#020617,#0f172a);
        border-radius: 16px;
        padding: 22px;
        border: 1px solid rgba(56,189,248,0.25);
        box-shadow: 0 0 15px rgba(56,189,248,0.15);
    }

    .cap-title {
        font-size: 16px;
        font-weight: 600;
        color: #38bdf8;
        margin-bottom: 6px;
    }

    /* ================= DEVELOPER ================= */
    .dev-name {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg,#38bdf8,#0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .dev-role {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 18px;
    }

    /* ================= BUTTONS ================= */
    .btn-group {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }

    .btn {
        padding: 12px 28px;
        border-radius: 14px;
        font-weight: 600;
        text-decoration: none;
        color: white;
        background: linear-gradient(90deg,#38bdf8,#0ea5e9);
        box-shadow: 0 0 18px rgba(56,189,248,0.5);
        transition: 0.3s;
    }

    .btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 28px rgba(56,189,248,0.8);
    }

    /* ================= FOOTER ================= */
    .footer {
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
        color: #94a3b8;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="container">', unsafe_allow_html=True)

    # HEADER
    st.markdown('<div class="hero-title">Sign Language Detection System</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Real-Time AI-Based Hand Gesture Recognition Project</div>', unsafe_allow_html=True)

    # OVERVIEW
    st.markdown('<div class="card"><div class="section-title">Project Overview</div><div class="text">This project detects and classifies sign language gestures in real-time using Artificial Intelligence and Computer Vision. It captures webcam input, processes hand landmarks using MediaPipe, and predicts gestures through a trained deep learning model. The system converts detected signs into readable text and speech, reducing communication barriers.</div></div>', unsafe_allow_html=True)

    # HIGHLIGHTS
    st.markdown('<div class="card"><div class="section-title">Platform Highlights</div><div class="stats">'
                '<div class="stat-box"><div class="stat-num">26+</div><div class="stat-label">Hand Signs</div></div>'
                '<div class="stat-box"><div class="stat-num">95%</div><div class="stat-label">Model Accuracy</div></div>'
                '<div class="stat-box"><div class="stat-num">Real-Time</div><div class="stat-label">Detection</div></div>'
                '<div class="stat-box"><div class="stat-num">AI</div><div class="stat-label">Powered</div></div>'
                '</div></div>', unsafe_allow_html=True)

    # CAPABILITIES
    st.markdown('<div class="card"><div class="section-title">Core Capabilities</div><div class="cap-grid">'
                '<div class="cap-box"><div class="cap-title">Live Gesture Detection</div>Real-time webcam-based detection.</div>'
                '<div class="cap-box"><div class="cap-title">AI Classification</div>Deep learning powered sign recognition.</div>'
                '<div class="cap-box"><div class="cap-title">Text & Voice Output</div>Convert gestures into readable output.</div>'
                '<div class="cap-box"><div class="cap-title">Analytics & History</div>Stores detection history for review.</div>'
                '</div></div>', unsafe_allow_html=True)

    # TECH STACK (MAIN ONLY)
    st.markdown('<div class="card"><div class="section-title">Technology Stack</div><div class="text">Python • Streamlit • OpenCV • MediaPipe • TensorFlow • Keras  • Flask  • Text-to-Speech • SQLite, JSON  </div></div>', unsafe_allow_html=True)

    # DEVELOPER
    st.markdown('<div class="card">'
                '<div class="section-title">Developer</div>'
                '<div class="dev-name">Himanshu Choudhary</div>'
                '<div class="dev-role">Data Analytics | AI & Computer Vision Developer</div>'
                '<div class="btn-group">'
                '<a class="btn" href="https://www.linkedin.com/in/himanshu-choudhary-data-analytics/" target="_blank">LinkedIn</a>'
                '<a class="btn" href="https://github.com/HimanshuChoudhary14" target="_blank">GitHub</a>'
                '</div></div>', unsafe_allow_html=True)

    # FOOTER MESSAGE
    st.markdown('<div class="footer">Building intelligent systems that create meaningful social impact through technology.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)