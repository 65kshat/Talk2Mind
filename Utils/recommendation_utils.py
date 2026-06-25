def generate_recommendations(wellbeing_score, risk_level, visual_emotion, speech_emotion, questionnaire_level):

    recommendations = []

    if risk_level == "Critical":
        recommendations.extend([
            "Consider seeking professional mental health support.",
            "Speak with a trusted friend, family member, or counselor.",
            "Maintain regular sleep and meal schedules.",
            "Reduce exposure to stressful situations where possible."
        ])

    elif risk_level == "Poor":
        recommendations.extend([
            "Practice mindfulness or meditation daily.",
            "Engage in at least 30 minutes of physical activity.",
            "Spend time with supportive people.",
            "Monitor emotional changes regularly."
        ])

    elif risk_level == "Moderate":
        recommendations.extend([
            "Maintain a healthy daily routine.",
            "Exercise regularly.",
            "Take regular breaks from work or study.",
            "Continue monitoring your emotional well-being."
        ])

    elif risk_level == "Good":
        recommendations.extend([
            "Maintain your current healthy habits.",
            "Continue exercising and socializing regularly.",
            "Practice gratitude and self-reflection."
        ])

    else:
        recommendations.extend([
            "Excellent mental well-being detected.",
            "Continue your current healthy lifestyle.",
            "Maintain positive routines and relationships."
        ])

    if visual_emotion == "Sad":
        recommendations.append("Engage in enjoyable activities that improve mood.")

    elif visual_emotion == "Anger":
        recommendations.append("Practice relaxation and anger-management techniques.")

    elif visual_emotion == "Fear":
        recommendations.append("Use breathing exercises and grounding techniques.")

    if speech_emotion == "Sad":
        recommendations.append("Reach out to supportive friends or family members.")

    elif speech_emotion == "Fearful":
        recommendations.append("Consider stress-management exercises.")

    elif speech_emotion == "Angry":
        recommendations.append("Take breaks and avoid emotionally charged situations.")

    if questionnaire_level in ["Severe", "Extremely Severe"]:

        recommendations.append("Professional counseling is strongly recommended.")

    return list(set(recommendations))