from streamlit import exception, info, session_state, set_page_config, title

from naturalizz.app_actions import (
    init_session,
)

from .data_display import display_data_section
from .input_widgets import (
    answer_state_input,
    launch_button,
    reveal_data_button,
    selection_bar,
)
from .score_counter import score_counter


def app() -> None:
    """Generate app's full display."""
    set_page_config(layout="wide")
    init_session()

    title("Naturalizz", anchor=False)
    score_counter()
    selection_bar()

    try:
        display_data_section()
        if session_state.data and not session_state.reveal_data:
            rank_for_display = " or ".join(
                session_state.data["data_used_for_search"]["rank_filter"],
            )

            info(
                f"You are currently looking for a **{rank_for_display}**",
                icon="ℹ️",
            )
        reveal_data_button()
        launch_button()
        answer_state_input()
    except Exception as e:
        exception(e)
        session_state.ready_to_restart = True
        launch_button()
