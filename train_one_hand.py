print("Training Script Start")

import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# LOAD DATA
data = pd.read_csv("../../data/landmarks_one_hand.csv")


print("Dataset Loaded")

X = data.drop("label", axis=1).values.astype("float32")
y = data["label"].values

# LABEL ENCODING
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_cat = to_categorical(y_encoded)

with open("label_encoder_one_hand.pkl", "wb") as f:
    pickle.dump(encoder, f)

# SCALING
scaler = StandardScaler()
X = scaler.fit_transform(X)

with open("scaler_one_hand.pkl", "wb") as f:
    pickle.dump(scaler, f)

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, random_state=42
)

# MODEL
model = Sequential([
    Input(shape=(X.shape[1],)),
    Dense(256, activation="relu"),
    Dropout(0.3),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dense(y_cat.shape[1], activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training Started")

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=32,
    callbacks=[early_stop]
)

loss, accuracy = model.evaluate(X_test, y_test)

print("Final Accuracy:", accuracy)

model.save("gesture_model_one_hand.h5")

print("Model Saved")
