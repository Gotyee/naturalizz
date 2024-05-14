import streamlit as st

from naturalizz.app_actions import (
    display_images,
    display_results,
    fill_text_field_with_data,
    init_session,
    quizz_starter,
)

init_session()

st.title("Naturalizz", anchor=False)
with st.container():
    config_choice = (
        st.radio(
            label="Select which configuration to use",
            options=["ALL", "Insect", "Plant"],
            horizontal=True,
            key="config_choice",
        ),
    )


with st.container():
    launch_pic = st.button(
        "Launch picture",
        key="launch_pic",
        use_container_width=True,
    )

try:
    if launch_pic:
        quizz_starter()
    image = display_images()
    results = display_results()
    if not st.session_state.reveal_data and st.session_state.show:
        st.button(
            "Click to Hide/Reveal Text",
            on_click=fill_text_field_with_data,
        )
except Exception as e:
    st.error(e)
    launch_pic = False
