import cv2
import mediapipe as mp
import csv
import os

DATA_DIR = "../data"
CSV_FILE = os.path.join(DATA_DIR, "landmarks_one_hand.csv")

os.makedirs(DATA_DIR, exist_ok=True)

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

saving = False

# Finger Colors
FINGER_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255)
]

if not cap.isOpened():
    print("Camera error")
    exit()

# ===== CSV HEADER =====
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        header = []
        for i in range(21):
            header += [f"x{i}", f"y{i}", f"z{i}"]
        header.append("label")
        writer.writerow(header)

with mp_hands.Hands(max_num_hands=1) as hands:

    while True:

        GESTURE_NAME = input("\nEnter gesture name (or exit): ")

        if GESTURE_NAME.lower() == "exit":
            break

        while True:

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            hand_data = None

            if results.multi_hand_landmarks:
                lm = results.multi_hand_landmarks[0].landmark

                cx, cy = int(lm[0].x * w), int(lm[0].y * h)
                cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)

                fingers = [
                    [1,2,3,4],
                    [5,6,7,8],
                    [9,10,11,12],
                    [13,14,15,16],
                    [17,18,19,20]
                ]

                for i, finger in enumerate(fingers):
                    px, py = cx, cy
                    for idx in finger:
                        x, y = int(lm[idx].x * w), int(lm[idx].y * h)
                        cv2.circle(frame, (x, y), 5, FINGER_COLORS[i], -1)
                        cv2.line(frame, (px, py), (x, y), FINGER_COLORS[i], 2)
                        px, py = x, y

                lm_list = []
                for p in lm:
                    lm_list.extend([p.x, p.y, p.z])

                hand_data = lm_list

            # ===== SAVE ONLY WHILE S IS HELD =====
            if saving and hand_data:
                with open(CSV_FILE, "a", newline="") as f:
                    csv.writer(f).writerow(hand_data + [GESTURE_NAME])

                cv2.putText(frame, "Saving (Hold S)",
                            (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

            # ===== UI =====
            cv2.putText(frame, f"Gesture: {GESTURE_NAME}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            cv2.putText(frame, "Hold S = Save",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)

            cv2.putText(frame, "N = New Gesture",
                        (20, 170),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)

            cv2.putText(frame, "Q = Quit",
                        (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)

            cv2.imshow("One Hand Collection", frame)

            key = cv2.waitKey(1) & 0xFF

            # 🔑 HOLD-KEY LOGIC (IMPORTANT FIX)
            if key == ord("s"):
                saving = True
            else:
                saving = False

            if key == ord("n"):
                break

            elif key == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                exit()

cap.release()
cv2.destroyAllWindows()
