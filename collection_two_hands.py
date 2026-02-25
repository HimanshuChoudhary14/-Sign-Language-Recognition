import cv2
import mediapipe as mp
import csv
import os

DATA_DIR = "../data"
CSV_FILE = os.path.join(DATA_DIR, "landmarks_two_hands.csv")

os.makedirs(DATA_DIR, exist_ok=True)

mp_hands = mp.solutions.hands

FINGER_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255)
]

cap = cv2.VideoCapture(0)

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

        print("Press S to save | N for new gesture | Q to quit program")

        while True:

            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            left_hand = [0]*63
            right_hand = [0]*63

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(
                        results.multi_hand_landmarks,
                        results.multi_handedness):

                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    lm_list = []
                    for lm in hand_landmarks.landmark:
                        lm_list.extend([lm.x, lm.y, lm.z])

                    label = handedness.classification[0].label

                    if label == "Left":
                        left_hand = lm_list
                    else:
                        right_hand = lm_list

            cv2.putText(frame, f"Gesture: {GESTURE_NAME}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

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

