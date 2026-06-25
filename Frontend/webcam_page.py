import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)

import streamlit as st
from config import VISUAL_MODEL_PATH #type: ignore

from Utils.visual_utils import (load_visual_model, analyze_session, get_visual_wellbeing_score, EMOTION_LABELS)
from assesment_scripts import (get_random_script) #type: ignore


@st.cache_resource
def get_visual_model():
    return load_visual_model(VISUAL_MODEL_PATH)

def show_webcam_page():
    st.header("Facial Emotion Analysis")

    if "assessment_script" not in st.session_state:
        st.session_state.assessment_script = (get_random_script())

    st.subheader("Assessment Reading Task")
    st.info(st.session_state.assessment_script)

    st.warning(
        """
        Please read the passage above naturally.

        Maintain eye contact with the camera whenever possible.

        Press ESC on your keyboard if you wish to finish early.
        """
    )

    model = get_visual_model()
    st.success("Visual Model Loaded Successfully")

    if st.button("Start Facial Assessment"):
        try:
            with st.spinner("Running Facial Assessment..."):
                results = analyze_session(model=model, duration_seconds=30, frame_interval=2)

            average_probabilities = (results["average_probabilities"])
            visual_score = (get_visual_wellbeing_score(average_probabilities))
            st.session_state.visual_score = (visual_score)
            st.session_state.visual_results = (results)

            st.success("Facial Analysis Complete")

        except Exception as e:
            st.error(f"Error: {e}")

    if "visual_score" in st.session_state:
        st.metric("Visual Wellbeing Score", st.session_state.visual_score)
        st.write("Frames Analyzed:", st.session_state.visual_results["samples_analyzed"])
        st.subheader("Emotion Distribution")

        probabilities = (st.session_state.visual_results["average_probabilities"])

        for emotion, prob in zip(EMOTION_LABELS, probabilities):
            st.progress(float(prob))
            st.write(f"{emotion}: {prob * 100:.2f}%")