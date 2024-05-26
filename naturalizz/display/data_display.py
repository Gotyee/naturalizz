from streamlit import columns, container, empty, markdown, session_state, write
from streamlit.delta_generator import DeltaGenerator

from naturalizz.app_actions import (
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


def _images_section() -> DeltaGenerator:
    """Display images to user after data has been fetched."""
    if not session_state.data:
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


def _results_section() -> DeltaGenerator:
    """Show results to user if reveal button has been pressed."""
    if not session_state.reveal_data:
        return empty()
    result_container = container()
    with result_container:
        for rank in RANKS:
            write(session_state[rank])

    return result_container


def display_data_section() -> None:
    """Display images related to taxon and its data, plus the reveal button."""
    # prevent result skip if misclicked
    if session_state.get("launch_pic") and session_state.ready_to_restart:
        quizz_starter()

    _images_section()
    _results_section()
