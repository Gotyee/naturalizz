from streamlit import (
    button,
    container,
    radio,
    session_state,
)

from naturalizz.app_actions import (
    fill_text_field_with_data,
)
from naturalizz.configuration import TAXON_TYPE


def selection_bar() -> None:
    """Display availables filter options."""
    with container():
        (
            radio(
                label="Select which configuration to use",
                options=[value for _, value in TAXON_TYPE.items()],
                horizontal=True,
                key="config_choice",
            ),
        )


def launch_button() -> None:
    """Display quizz start button."""
    with container():
        button(
            "Launch picture",
            key="launch_pic",
            use_container_width=True,
        )


def reveal_data_button() -> None:
    """Display or not the reveal data button."""
    if not session_state.reveal_data and session_state.data:
        button(
            "Click to Hide/Reveal Text",
            on_click=fill_text_field_with_data,
            key="reveal_data_button",
        )


def answer_state_input() -> None:
    """Display or not radio widget to retrieve answer state (correct or not)."""
    if not session_state.answer and session_state.reveal_data:
        (
            radio(
                label="How did you answer the quizz?",
                options=["Correct", "Wrong"],
                horizontal=True,
                key="answer",
            ),
        )
