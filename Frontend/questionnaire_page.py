import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st

from config import QUESTIONNAIRE_MODEL_PATH #type: ignore

from Utils.questionnaire_utils import (load_questionnaire_model, predict_questionnaire)


@st.cache_resource
def get_questionnaire_model():
    return load_questionnaire_model(QUESTIONNAIRE_MODEL_PATH)

def show_questionnaire_page():
    st.header("Mental Health Questionnaire")
    st.markdown("""
    ### Instructions

    Please read each statement carefully and select the option
    that best describes how much the statement applied to you
    during the past week.

    There are no right or wrong answers.
    """)

    model = get_questionnaire_model()

    st.success("Questionnaire Model Loaded Successfully")

    DASS_OPTIONS = {
        "Did not apply to me at all": 0,
        "Applied to me to some degree, or some of the time": 1,
        "Applied to me to a considerable degree, or a good part of the time": 2,
        "Applied to me very much, or most of the time": 3
    }

    st.subheader("Demographic Information") 
    q1_1 = st.number_input("Age", min_value=16, max_value=100)
    gender_text = st.selectbox("Gender", ["Male", "Female"])
    q1_2 = 0 if gender_text == "Male" else 1
    
    st.divider()

    st.subheader("Stress Assessment")

    stress_questions = [
        "I found it hard to wind down",
        "I tended to over-react to situations",
        "I felt that I was using a lot of nervous energy",
        "I found myself getting agitated",
        "I found it difficult to relax",
        "I was intolerant of anything that kept me from getting on with what I was doing",
        "I felt that I was rather touchy"
    ]

    stress_answers = []

    for idx, question in enumerate(stress_questions, start=1):
        response = st.radio(f"{idx}. {question}", options=list(DASS_OPTIONS.keys()), key=f"stress_{idx}")
        stress_answers.append(DASS_OPTIONS[response])

    stress_score = sum(stress_answers)
    st.info(f"Stress Score: {stress_score}")

    st.divider()

    st.subheader("Anxiety Assessment")

    anxiety_questions = [
        "I was aware of dryness of my mouth",
        "I experienced breathing difficulty",
        "I experienced trembling",
        "I was worried about situations in which I might panic and make a fool of myself",
        "I felt I was close to panic",
        "I was aware of the action of my heart in the absence of physical exertion",
        "I felt scared without any good reason"
    ]

    anxiety_answers = []

    for idx, question in enumerate(anxiety_questions, start=1):
        response = st.radio(f"{idx}. {question}", options=list(DASS_OPTIONS.keys()), key=f"anxiety_{idx}")
        anxiety_answers.append(DASS_OPTIONS[response])

    anxiety_score = sum(anxiety_answers)

    st.info(f"Anxiety Score: {anxiety_score}")
    st.divider()

    st.subheader("Depression Assessment")

    depression_questions = [
        "I couldn't seem to experience any positive feeling at all",
        "I found it difficult to work up the initiative to do things",
        "I felt that I had nothing to look forward to",
        "I felt down-hearted and blue",
        "I was unable to become enthusiastic about anything",
        "I felt I wasn't worth much as a person",
        "I felt that life was meaningless"
    ]

    depression_answers = []

    for idx, question in enumerate(depression_questions, start=1):
        response = st.radio(f"{idx}. {question}", options=list(DASS_OPTIONS.keys()), key=f"depression_{idx}")
        depression_answers.append(DASS_OPTIONS[response])

    depression_score = sum(depression_answers)

    st.info(f"Depression Score: {depression_score}")
    st.divider()

    if st.button("Analyze Questionnaire"):

        feature_vector = [
            q1_1, q1_2, 0, 0, 0, 0, 
            *stress_answers, stress_score,
            *anxiety_answers, anxiety_score,
            *depression_answers, depression_score
        ]

        level, confidence, probs = (predict_questionnaire(feature_vector, model))

        st.session_state.questionnaire_level = (level)
        st.session_state.questionnaire_confidence = (confidence)
        st.session_state.questionnaire_probs = (probs)

        st.session_state.questionnaire_score = (max(0, 100 - (depression_score * 2)))

        st.success("Questionnaire Analysis Complete")

        st.metric("Predicted Level", level)

        st.metric("Confidence", f"{confidence:.2%}")