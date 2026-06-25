import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

LEVEL_LABELS = ["Normal", "Mild", "Moderate", "Severe", "Extremely Severe"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class QuestionnaireNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(30, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 5)
        )

    def forward(self, x):
        return self.network(x)


def load_questionnaire_model(model_path):
    model = QuestionnaireNN()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()

    return model


def preprocess_questionnaire(responses):
    responses = np.array(responses, dtype=np.float32)
    responses = torch.tensor(responses, dtype=torch.float32)
    responses = responses.unsqueeze(0)

    return responses


def predict_questionnaire(responses, model):
    responses = preprocess_questionnaire(responses)
    responses = responses.to(device)

    with torch.no_grad():

        outputs = model(responses)
        probabilities = F.softmax(outputs, dim=1)

    probabilities = (probabilities.cpu().numpy()[0])
    predicted_index = np.argmax(probabilities)
    predicted_level = (LEVEL_LABELS[predicted_index])
    confidence = float(probabilities[predicted_index])

    return (predicted_level, confidence, probabilities)


def get_questionnaire_wellbeing_score(probabilities):

    weights = np.array([100, 75, 50, 25, 0])
    score = np.sum(probabilities * weights)

    return round(float(score), 2)