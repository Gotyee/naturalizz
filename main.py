import streamlit as st
from PIL import Image

from naturalizz.configuration import init_session, reset_session
from naturalizz.data_retrieval import random_taxon, retrieve_taxon_data

init_session()


def picture_launcher():
    reset_session()
    st.session_state.hide = not st.session_state.hide
    st.session_state.data = retrieve_taxon_data(taxon_name=random_taxon())


def reveal_label():
    print(st.session_state.data)
    st.session_state.name = f"Nom complet: {st.session_state.data['name']} \n"
    st.session_state.order = f"Ordre: {st.session_state.data['order']}"
    st.session_state.family = f"Famille: {st.session_state.data['family']}"
    st.session_state.genus = f"Genre: {st.session_state.data['genus']}"
    st.session_state.species = f"Espèce: {st.session_state.data['species']}"
    st.session_state.label_reveal = True


st.title("Naturalist quizz", anchor=False)
c1, c2, c3 = st.columns(3)
with st.container():
    with c1:
        st.button("Default configuration", key="default")
    c2.write("c2")

with st.container():
    st.button(
        "Launch picture",
        key="launch_pic",
        on_click=picture_launcher,
        use_container_width=True,
    )

if st.session_state.hide:
    secret = st.container()
    with secret:
        image = st.session_state.data["photo"].open()
        max_height = 400  # Adjust this value according to your requirement
        image = Image.open(image)
        # Calculate the width proportionally to maintain the aspect ratio
        width, height = image.size
        aspect_ratio = width / height
        new_width = int(max_height * aspect_ratio)

        st.image(image, width=new_width)
        st.write(st.session_state.order)
        st.write(st.session_state.family)
        st.write(st.session_state.genus)
        st.write(st.session_state.species)
        st.write(st.session_state.name)
        if not st.session_state.label_reveal:
            st.button("Click to Hide/Reveal Text", on_click=reveal_label)
