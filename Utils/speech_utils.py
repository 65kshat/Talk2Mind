import torch
import torch.nn as nn
import torch.nn.functional as F

import librosa
import sounddevice as sd  # type: ignore
import soundfile as sf    # type: ignore

import numpy as np
from collections import Counter

EMOTION_LABELS = ["Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Attention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attention = nn.Linear(hidden_size * 2, 1)

    def forward(self, lstm_output):
        attention_weights = torch.softmax(self.attention(lstm_output), dim=1)
        context_vector = torch.sum(attention_weights * lstm_output, dim=1)

        return context_vector

class AttentionBiLSTM(nn.Module):
    def __init__(self, input_size=42, hidden_size=128, num_layers=2, num_classes=8, dropout=0.4):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True, bidirectional=True, dropout=dropout)
        self.attention = Attention(hidden_size)
        self.dropout = nn.Dropout(dropout)

        self.fc1 = nn.Linear(hidden_size * 2, 256)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, num_classes)

    def forward(self, x):
        lstm_output, _ = self.lstm(x)
        context_vector = self.attention(lstm_output)

        x = self.dropout(context_vector)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)

        return x

def load_speech_model(model_path):
    model = AttentionBiLSTM()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    return model

def record_audio(duration=10, sample_rate=22050, output_file="recorded_audio.wav"):
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    
    sd.wait()
    sf.write(output_file, recording, sample_rate)

    return output_file

def extract_features(audio_path):
    signal, sr = librosa.load(audio_path, sr=22050)
    
    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)
    rms = librosa.feature.rms(y=signal)
    zcr = librosa.feature.zero_crossing_rate(signal)

    TARGET_LENGTH = 150

    mfcc = mfcc[:, :TARGET_LENGTH]
    rms = rms[:, :TARGET_LENGTH]
    zcr = zcr[:, :TARGET_LENGTH]

    if mfcc.shape[1] < TARGET_LENGTH:
        pad = TARGET_LENGTH - mfcc.shape[1]

        mfcc = np.pad(mfcc, ((0, 0), (0, pad)))
        rms = np.pad(rms, ((0, 0), (0, pad)))
        zcr = np.pad(zcr, ((0, 0), (0, pad)))

    combined = np.vstack([mfcc, rms, zcr])
    combined = combined.T

    return combined.astype(np.float32)

def predict_speech(audio_path, model):
    features = extract_features(audio_path)
    features = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    features = features.to(device)

    print("\nFeature Mean:", np.mean(features.cpu().numpy()))
    print("Feature Std:", np.std(features.cpu().numpy()))
    print("Feature Min:", np.min(features.cpu().numpy()))
    print("Feature Max:", np.max(features.cpu().numpy()))

    with torch.no_grad():
        outputs = model(features)
        probabilities = F.softmax(outputs, dim=1)

    probabilities = (probabilities.cpu().numpy()[0])
    predicted_index = np.argmax(probabilities)
    predicted_emotion = (EMOTION_LABELS[predicted_index])

    print("\n========== PREDICTION ==========")
    print("Predicted Emotion:", predicted_emotion)

    for emotion, prob in zip(EMOTION_LABELS, probabilities):
        print(f"{emotion}: {prob:.4f}")

    return (predicted_emotion, probabilities)

def analyze_speech_session(audio_files, model):
    emotion_history = []
    probability_history = []

    for audio_file in audio_files:
        emotion, probs = predict_speech(audio_file, model)
        emotion_history.append(emotion)
        probability_history.append(probs)

    probability_history = np.array(probability_history)
    average_probabilities = np.mean(probability_history, axis=0)

    dominant_emotion = Counter(emotion_history).most_common(1)[0][0]

    return {
        "dominant_emotion": dominant_emotion,
        "emotion_history": emotion_history,
        "average_probabilities": average_probabilities,
        "samples_analyzed": len(emotion_history)
    }

def get_speech_wellbeing_score(average_probabilities):
    score = (
        (average_probabilities[2] * 100) +
        (average_probabilities[1] * 90) +
        (average_probabilities[0] * 70) +
        (average_probabilities[7] * 60) -

        (average_probabilities[3] * 40) -
        (average_probabilities[4] * 60) -
        (average_probabilities[5] * 50) -
        (average_probabilities[6] * 50))

    score = max(0, min(100, score + 50))
    return round(score, 2)