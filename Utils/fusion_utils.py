import numpy as np

def create_fusion_vector(visual_probs, speech_probs, questionnaire_probs):
    fusion_vector = np.concatenate([visual_probs, speech_probs, questionnaire_probs])

    return fusion_vector

def calculate_wellbeing_score(visual_score, speech_score, questionnaire_score):

    wellbeing_score = ((visual_score * 0.30) + (speech_score * 0.30) + (questionnaire_score * 0.40))
    wellbeing_score = max(0, min(100, wellbeing_score))

    return round(wellbeing_score, 2)

def classify_risk_level(wellbeing_score):
    if wellbeing_score >= 80:
        return "Excellent"

    elif wellbeing_score >= 60:
        return "Good"

    elif wellbeing_score >= 40:
        return "Moderate"

    elif wellbeing_score >= 20:
        return "Poor"

    else:
        return "Critical"


def generate_assessment(visual_score, speech_score, questionnaire_score):

    wellbeing_score = (calculate_wellbeing_score(visual_score, speech_score, questionnaire_score))
    risk_level = (classify_risk_level(wellbeing_score))

    return {
        "visual_score":
            visual_score,

        "speech_score":
            speech_score,

        "questionnaire_score":
            questionnaire_score,

        "wellbeing_score":
            wellbeing_score,

        "risk_level":
            risk_level
    }