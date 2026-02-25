import sqlite3

DB_NAME = "gesture_data.db"


# ================= SAFE CONNECTION =================
def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")   # 🔥 performance boost
    return conn


# ================= INIT TABLES =================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ---- detections table ----
    c.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gesture TEXT,
            confidence REAL,
            time TEXT
        )
    """)

    # ---- feedback table ----
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating TEXT,
            type TEXT,
            feedback TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()


# ================= DETECTIONS =================
def save_detection(gesture, confidence, time):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO detections (gesture, confidence, time)
        VALUES (?, ?, ?)
    """, (gesture, confidence, time))

    conn.commit()
    conn.close()


def fetch_all_detections():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT gesture, confidence, time
        FROM detections
        ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()
    return data


# ================= FEEDBACK =================
def save_feedback(rating, feedback_type, feedback_text, time):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO feedback (rating, type, feedback, time)
        VALUES (?, ?, ?, ?)
    """, (rating, feedback_type, feedback_text, time))

    conn.commit()
    conn.close()


def fetch_all_feedback():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT rating, type, feedback, time
        FROM feedback
        ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()
    return data