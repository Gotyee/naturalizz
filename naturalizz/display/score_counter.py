import streamlit as st
from streamlit import session_state

col1, col2 = st.columns(2)
with col1:
    col1.metric("Correct answers", "70 °F", "1.2 °F")
    expander = st.expander("See correct taxons")
    expander.dataframe(
        session_state.answer_data[session_state.answer_data["answer"]],
    )
with col2:
    col2.metric("Wrong answers", "70 °F", "1.2 °F")
    expander = st.expander("See wrong taxons")
    expander.dataframe(session_state.answer_data[~session_state.answer_data["answer"]])
