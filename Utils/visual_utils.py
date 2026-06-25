import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F

from torchvision.models import efficientnet_b0 #type: ignore
from torchvision import transforms #type: ignore

import numpy as np
from collections import Counter

EMOTION_LABELS = ["Anger", "Contempt", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise" ]

device = torch.device("cuda" if torch.cuda.is_available()else "cpu")

transform = transforms.Compose(
[
transforms.ToPILImage(),
transforms.Resize((224, 224)),
transforms.ToTensor()
]
)

def load_visual_model(model_path):
    model = efficientnet_b0(weights=None)
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, 8)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    return model

def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = transform(frame)
    frame = frame.unsqueeze(0)
    frame = frame.to(device)

    return frame

def predict_frame(frame, model):
    frame_tensor = preprocess_frame(frame)

    with torch.no_grad():
        outputs = model(frame_tensor)
        probabilities = F.softmax(outputs, dim=1)

    probabilities = (probabilities.cpu().numpy()[0])
    emotion_index = np.argmax(probabilities)
    emotion = EMOTION_LABELS[emotion_index]
    confidence = float(probabilities[emotion_index])

    return (emotion, confidence, probabilities)

def analyze_session(model, duration_seconds=60, frame_interval=2):

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Unable to access webcam.")

    emotion_history = []
    probability_history = []
    start_time = cv2.getTickCount()
    fps = cv2.getTickFrequency()
    next_capture = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        elapsed = (cv2.getTickCount() - start_time) / fps

        if elapsed >= next_capture:
            emotion, confidence, probs = (predict_frame(frame, model))
            emotion_history.append(emotion)
            probability_history.append(probs)
            next_capture += frame_interval

        cv2.imshow("Talk2Mind Camera Session", frame)

        if elapsed >= duration_seconds:
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    probability_history = np.array(probability_history)
    average_probabilities = np.mean(probability_history, axis=0)
    dominant_emotion = Counter(emotion_history).most_common(1)[0][0]

    return {
        "dominant_emotion": dominant_emotion,
        "emotion_history": emotion_history,
        "average_probabilities": average_probabilities,
        "samples_analyzed": len(emotion_history)
    }

def get_visual_wellbeing_score(average_probabilities):

    happy_score = (average_probabilities[4])
    neutral_score = (average_probabilities[5])
    sad_score = (average_probabilities[6])
    fear_score = (average_probabilities[3])
    anger_score = (average_probabilities[0])

    score = ((happy_score * 50) + (neutral_score * 30) - (sad_score * 20 ) - (fear_score * 10) - (anger_score * 10))
    score = max(0, min(100, score + 50))
    return round(score, 2)