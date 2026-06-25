import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    
import streamlit as st

from webcam_page import show_webcam_page #type: ignore
from audio_page import show_audio_page #type: ignore
from questionnaire_page import show_questionnaire_page #type: ignore
from results_page import show_results_page #type: ignore

st.set_page_config(page_title="Talk2Mind", layout="wide")

st.title("Talk2Mind")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Facial Analysis",
        "Speech Analysis",
        "Questionnaire",
        "Results"
    ]
)

with tab1:
    show_webcam_page()

with tab2:
    show_audio_page()

with tab3:
    show_questionnaire_page()

with tab4:
    show_results_page()