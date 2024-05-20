from streamlit import (
    button,
    columns,
    container,
    empty,
    markdown,
    radio,
    session_state,
    write,
)
from streamlit.delta_generator import DeltaGenerator

from naturalizz.app_actions import (
    fill_text_field_with_data,
    quizz_starter,
    retrieve_and_resize_img_list,
)
from naturalizz.configuration import NB_PIC_DISPLAYED, RANKS

HIDE_IMG_FS_OPTION = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""


def display_images() -> DeltaGenerator:
    """Display images to user."""
    if not session_state.show:
        return empty()
    images_container = container()
    image_cols = columns(NB_PIC_DISPLAYED)
    with images_container:
        for col, image in zip(
            image_cols,
            retrieve_and_resize_img_list(session_state.data["photo"]),
            strict=True,
        ):
            col.image(image)
    markdown(HIDE_IMG_FS_OPTION, unsafe_allow_html=True)
    return images_container


def display_results() -> DeltaGenerator:
    """Show results to user if reveal button has been pressed."""
    if not session_state.reveal_data:
        return empty()
    result_container = container()
    with result_container:
        for rank in RANKS:
            write(session_state[rank])
    return result_container


def display_selection_bar_and_launch_button() -> None:
    """Display avaiables filter options and quizz start button."""
    with container():
        (
            radio(
                label="Select which configuration to use",
                options=["ALL", "Insect", "Plant"],
                horizontal=True,
                key="config_choice",
            ),
        )

    with container():
        button(
            "Launch picture",
            key="launch_pic",
            use_container_width=True,
        )


def display_image_and_result() -> None:
    if session_state.launch_pic:
        quizz_starter()
    display_images()
    display_results()
    if not session_state.reveal_data and session_state.show:
        button(
            "Click to Hide/Reveal Text",
            on_click=fill_text_field_with_data,
        )