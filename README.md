# ✋ Sign Language Detection & Recognition System

## 📌 Project Summary
The Sign Language Detection & Recognition System is an AI-based application developed as a Major Project for academic submission. The system is designed to recognize hand gestures in real time using a webcam and convert them into meaningful text and voice output. This project aims to reduce the communication gap between hearing-impaired individuals and others by leveraging Artificial Intelligence and Computer Vision technologies.

The application captures live video input, extracts hand landmarks, processes them using a trained deep learning model, and predicts the corresponding sign. The recognized gesture is displayed as text on the screen and converted into speech using a text-to-speech engine. The project follows a modular architecture for better scalability, maintainability, and clean code organization.

---

## 🎓 Academic Purpose
This project is submitted as a Major Project for college evaluation. It demonstrates practical implementation of Artificial Intelligence, Deep Learning, and Computer Vision concepts in solving real-world problems.

---

## 🧠 Key Features
- Real-time gesture detection using webcam  
- One-hand sign language recognition  
- Landmark-based gesture classification  
- Deep Learning model integration  
- Text output of recognized gestures  
- Voice output using Text-to-Speech  
- Detection history storage using SQLite  
- Modular and scalable code structure  

---

## 🛠️ Technologies Used (Detailed Explanation)

### 1️⃣ Python
Python is used as the core programming language for developing the entire system. It provides strong support for AI, machine learning, and computer vision libraries. All application logic, model integration, and UI handling are implemented using Python.

### 2️⃣ OpenCV
OpenCV is used for:
- Capturing real-time video from webcam  
- Frame processing and image handling  
- Converting video frames into a format suitable for landmark extraction  

It plays a key role in enabling real-time gesture detection.

### 3️⃣ MediaPipe
MediaPipe is used for hand landmark detection.  
It detects 21 key hand landmarks from each frame and provides coordinate values.  
These landmark coordinates are used as input features for training and prediction in the deep learning model.

### 4️⃣ TensorFlow / Keras
TensorFlow and Keras are used to:
- Build and train the deep learning model  
- Perform gesture classification  
- Load the trained `.h5` model for real-time prediction  

The trained model identifies hand gestures based on landmark patterns.

### 5️⃣ Scikit-learn
Scikit-learn is used for:
- Label encoding of gesture classes  
- Feature scaling using a scaler  
- Preprocessing the landmark dataset before model training  

It helps improve model accuracy and consistency.

### 6️⃣ SQLite
SQLite is used as a lightweight local database to:
- Store detection history  
- Maintain user interaction records  
- Save gesture prediction logs  

It ensures data persistence without requiring an external database server.

### 7️⃣ Text-to-Speech (TTS)
The voice engine converts recognized gesture text into audio output.  
This feature makes the system more accessible and interactive for real-world usage.

---

## 📂 Project Structure

SIGN_LANGUAGE_DETECTION/
├── app/
│   ├── assets/
│   ├── learning__center/
│   │   └── ui.py
│   ├── Model/
│   │   ├── train_one_hand.py
│   │   ├── label_encoder_one_hand.pkl
│   │   ├── gesture_model_one_hand.h5
│   │   └── scaler_one_hand.pkl
│   ├── modules/
│   │   ├── model_loader.py
│   │   ├── detection.py
│   │   ├── database.py
│   │   └── voice_engine.py
│   ├── ui/
│   │   ├── dashboard.py
│   │   ├── feedback.py
│   │   ├── history.py
│   │   ├── styles.py
│   │   └── voice_settings.py
│   └── app.py
│
├── data/
│   ├── landmarks_one_hand.csv
│   
│
├── scripts/
│   ├── collection_one_hand.py
│   ├── collection_two_hands.py
│   ├── test_two_hand_detection.py
│   
│
├── requirements.txt
 
 

---

## 📊 Dataset Information
The dataset is stored in CSV format and consists of hand landmark coordinates extracted using MediaPipe. Each row represents a gesture sample with scaled landmark values and corresponding labels. The dataset is used to train the deep learning model for gesture classification.

---

## 🚀 How to Run the Project

Step 1: Clone the repository  
git clone https://github.com/your-username/SIGN_LANGUAGE_DETECTION.git  

Step 2: Install dependencies  
pip install -r requirements.txt  

Step 3: Run the application  
python app/app.py  

Ensure that a webcam is connected before running the system.

---

## 📈 Future Scope
- Two-hand gesture recognition  
- Sentence-level gesture translation  
- Mobile application version  
- Cloud deployment  
- Support for regional sign languages  

---

## 👨‍🎓 Developer
Name: Himanshu Choudhary  
Project Type: Major Project  
Domain: Artificial Intelligence & Computer Vision  

---

## 📜 License
This project is developed strictly for academic and educational purposes.
