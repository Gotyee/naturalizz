import streamlit as st
from streamlit import session_state

from naturalizz.app_actions import store_answers_state


def score_counter() -> None:
    if session_state.get("answer") and session_state.get("launch_pic"):
        store_answers_state()
    if session_state.answer_data.empty:
        return
    col1, col2 = st.columns(2)
    with col1:
        df_to_display = session_state.answer_data[session_state.answer_data["answer"]]
        df_to_display = df_to_display.drop(columns=["answer"])

        col1.metric(
            "Correct answers",
            len(df_to_display),
            f"{len(df_to_display)/len(session_state.answer_data) * 100} %",
        )
        expander = st.expander("See correct taxons")

        expander.dataframe(df_to_display)
    with col2:
        df_to_display = session_state.answer_data[~session_state.answer_data["answer"]]
        df_to_display = df_to_display.drop(columns=["answer"])

        col2.metric(
            "Wrong answers",
            len(df_to_display),
            f"{len(df_to_display)/len(session_state.answer_data) * 100} %",
            delta_color="inverse",
        )
        expander = st.expander("See incorrect taxons")
        expander.dataframe(df_to_display)
