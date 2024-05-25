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


def app() -> None:
    """Generate app's full display."""
    set_page_config(layout="wide")
    init_session()

    title("Naturalizz", anchor=False)

    selection_bar()
    if session_state.data:
        info(
            "You are currently looking for a "
            f"{session_state.data['data_used_for_search']['rank_filter']}",
            icon="ℹ️",
        )
    try:
        display_data_section()
        reveal_data_button()
        launch_button()
        answer_state_input()
    except Exception as e:
        exception(e)
