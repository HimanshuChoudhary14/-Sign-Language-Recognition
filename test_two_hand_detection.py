import cv2
import mediapipe as mp
import csv
import os

DATA_DIR = "../data"
CSV_FILE = os.path.join(DATA_DIR, "landmarks_two_hands.csv")

os.makedirs(DATA_DIR, exist_ok=True)

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

# Finger Colors
FINGER_COLORS = [
    (255, 0, 0),    # Thumb
    (0, 255, 0),    # Index
    (0, 255, 255),  # Middle
    (0, 0, 255),    # Ring
    (255, 0, 255)   # Pinky
]

if not cap.isOpened():
    print("Camera error")
    exit()

# CSV header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        header = []
        for hand in ["L", "R"]:
            for i in range(21):
                header += [f"{hand}_x{i}", f"{hand}_y{i}", f"{hand}_z{i}"]
        header.append("label")
        writer.writerow(header)

with mp_hands.Hands(max_num_hands=2) as hands:

    while True:

        GESTURE_NAME = input("\nEnter gesture name (or type exit): ")

        if GESTURE_NAME.lower() == "exit":
            break

        while True:

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            left_hand = [0]*63
            right_hand = [0]*63

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(
                        results.multi_hand_landmarks,
                        results.multi_handedness):

                    lm = hand_landmarks.landmark
                    label = handedness.classification[0].label

                    # Palm center
                    cx, cy = int(lm[0].x * w), int(lm[0].y * h)
                    cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)

                    fingers = [
                        [1, 2, 3, 4],
                        [5, 6, 7, 8],
                        [9, 10, 11, 12],
                        [13, 14, 15, 16],
                        [17, 18, 19, 20]
                    ]

                    # Draw colored skeleton
                    for i, finger in enumerate(fingers):
                        px, py = cx, cy
                        for idx in finger:
                            x, y = int(lm[idx].x * w), int(lm[idx].y * h)
                            cv2.circle(frame, (x, y), 5, FINGER_COLORS[i], -1)
                            cv2.line(frame, (px, py), (x, y),
                                     FINGER_COLORS[i], 2)
                            px, py = x, y

                    # Collect landmarks
                    lm_list = []
                    for p in lm:
                        lm_list.extend([p.x, p.y, p.z])

                    if label == "Left":
                        left_hand = lm_list
                        cv2.putText(frame, "LEFT", (cx-30, cy-20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (255,255,255),2)
                    else:
                        right_hand = lm_list
                        cv2.putText(frame, "RIGHT", (cx-30, cy-20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (255,255,255),2)

            # UI Text
            cv2.putText(frame, f"Gesture: {GESTURE_NAME}", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            cv2.putText(frame, "S = Save Sample", (20,80),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.putText(frame, "N = New Gesture", (20,110),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.putText(frame, "Q = Quit Program", (20,140),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

            cv2.imshow("Two Hand Collection", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                with open(CSV_FILE, "a", newline="") as f:
                    csv.writer(f).writerow(left_hand + right_hand + [GESTURE_NAME])
                print("Saved:", GESTURE_NAME)

            elif key == ord("n"):
                break

            elif key == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                exit()

cap.release()
cv2.destroyAllWindows()
