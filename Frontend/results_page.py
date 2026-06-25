import streamlit as st
from Utils.fusion_utils import (generate_assessment) #type: ignore
from Utils.recommendation_utils import (generate_recommendations) #type: ignore


def show_results_page():
    st.header("Mental Well-Being Assessment")

    if ("visual_score" not in st.session_state or st.session_state.visual_score is None):
        st.warning("Complete Facial Analysis first.")

        return

    if ("speech_score" not in st.session_state or st.session_state.speech_score is None):
        st.warning("Complete Speech Analysis first.")

        return

    if ("questionnaire_score" not in st.session_state or st.session_state.questionnaire_score is None):
        st.warning("Complete Questionnaire Assessment first.")

        return

    visual_score = (st.session_state.visual_score)
    speech_score = (st.session_state.speech_score)
    questionnaire_score = (st.session_state.questionnaire_score)

    visual_emotion = (st.session_state.get("visual_emotion", "Unknown"))
    speech_emotion = (st.session_state.get("speech_emotion", "Unknown"))
    questionnaire_level = (st.session_state.get("questionnaire_level", "Unknown"))

    assessment = (generate_assessment(visual_score, speech_score, questionnaire_score))
    wellbeing_score = (assessment["wellbeing_score"])

    risk_level = (assessment["risk_level"])

    recommendations = (
        generate_recommendations(
            wellbeing_score,
            risk_level,
            visual_emotion,
            speech_emotion,
            questionnaire_level
        )
    )

    st.subheader("Overall Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Well-Being Score", f"{wellbeing_score}/100")

    with col2:
        st.metric("Risk Level", risk_level)

    with col3:
        st.metric("Questionnaire Level", questionnaire_level)

    st.divider()
    st.subheader("Component Scores")
    st.progress(int(visual_score))

    st.write(f"Visual Score: {visual_score}")
    st.progress(int(speech_score))
    
    st.write(f"Speech Score: {speech_score}")
    st.progress(int(questionnaire_score))
    
    st.write(f"Questionnaire Score: {questionnaire_score}")

    st.divider()

    st.subheader("Personalized Recommendations")

    for recommendation in recommendations:
        st.write(f"• {recommendation}")

    st.divider()

    st.subheader( "Assessment Summary")
    st.success("This is the End Of Report for your Mental Health Well-Being")
        