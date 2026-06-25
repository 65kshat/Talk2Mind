import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)

import streamlit as st

from config import (SPEECH_MODEL_PATH) #type: ignore
from Utils.speech_utils import (load_speech_model, record_audio, analyze_speech_session, get_speech_wellbeing_score, EMOTION_LABELS)
from assesment_scripts import (get_random_script) #type: ignore

@st.cache_resource
def get_speech_model():
    return load_speech_model(SPEECH_MODEL_PATH)

def show_audio_page():
    st.header("Speech Emotion Analysis")
    if "assessment_script" not in st.session_state:
        st.session_state.assessment_script = (get_random_script())

    st.subheader("Assessment Reading Task")
    st.info(st.session_state.assessment_script)
    st.warning(
        """
        Please read the passage above clearly.

        Speak in a natural voice.

        Try to read every sentence completely.

        The recording duration can be adjusted below.
        """
    )

    model = get_speech_model()
    st.success("Speech Model Loaded Successfully")
    duration = st.slider("Recording Duration (seconds)", min_value=5, max_value=30, value=15)

    if st.button("Start Speech Assessment"):
        try:
            with st.spinner("Recording Audio..."):
                audio_file = record_audio(duration=duration)

            with st.spinner("Analyzing Speech..."):
                results = analyze_speech_session([audio_file], model)

            average_probabilities = (results["average_probabilities"])
            speech_score = (get_speech_wellbeing_score(average_probabilities))
            st.session_state.speech_score = (speech_score)
            st.session_state.speech_results = (results)
            st.success("Speech Analysis Complete")

        except Exception as e:
            st.error(f"Error: {e}")

    if "speech_score" in st.session_state:
        st.metric("Speech Wellbeing Score", st.session_state.speech_score)
        st.write("Samples Analyzed:", st.session_state.speech_results["samples_analyzed"])

        st.subheader("Emotion Distribution")
        probabilities = (st.session_state.speech_results["average_probabilities"])

        for emotion, prob in zip(EMOTION_LABELS, probabilities):
            st.progress(float(prob))
            st.write(f"{emotion}: {prob * 100:.2f}%")