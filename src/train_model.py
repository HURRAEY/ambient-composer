# train_model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np


# 딥러닝 모델을 설계하고 학습시키는 함수
def train_model(midi_data):
    model = Sequential()
    model.add(LSTM(128, input_shape=(50, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dense(100, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam")
    model.fit(midi_data, epochs=100, batch_size=64)
    model.save("granular_randomness_model.h5")


# 학습된 모델을 로드하고 무작위성을 조절하는 함수
def generate_randomness(midi_data, randomness_level):
    model = tf.keras.models.load_model("granular_randomness_model.h5")
    predictions = model.predict(midi_data) * randomness_level
    return predictions
