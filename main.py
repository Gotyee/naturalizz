import streamlit as st
from pyinstrument import Profiler

from naturalizz.app_actions import (
    fill_text_field_with_data,
    quizz_starter,
    retrieve_and_resize_img,
)
from naturalizz.configuration import init_session

profiler = Profiler()
profiler.start()
init_session()

st.title("Naturalist quizz", anchor=False)
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
    st.button(
        "Launch picture",
        key="launch_pic",
        on_click=quizz_starter,
        use_container_width=True,
    )

if st.session_state.hide:
    secret = st.container()
    with secret:
        # TODO: show 2-3 pictures
        st.image(retrieve_and_resize_img(st.session_state.data["photo"]))
        st.write(st.session_state.order)
        st.write(st.session_state.family)
        st.write(st.session_state.genus)
        st.write(st.session_state.species)
        st.write(st.session_state.name)
        if not st.session_state.label_reveal:
            st.button(
                "Click to Hide/Reveal Text",
                on_click=fill_text_field_with_data,
            )


profiler.stop()
# profiler.print()
