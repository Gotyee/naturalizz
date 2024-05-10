from streamlit import session_state


def init_session() -> None:
    """Init session_state parameters"""

    if "hide" not in session_state:
        session_state.hide = False

    if "data" not in session_state:
        session_state.data = None

    if "label_reveal" not in session_state:
        session_state.label_reveal = False

    if "name" not in session_state:
        session_state.name = ""

    if "order" not in session_state:
        session_state.order = ""

    if "family" not in session_state:
        session_state.family = ""

    if "genus" not in session_state:
        session_state.genus = ""

    if "species" not in session_state:
        session_state.species = ""


def reset_session() -> None:
    """Reset session_state parameters"""

    session_state.hide = False
    session_state.data = None
    session_state.label_reveal = False
    session_state.name = ""
    session_state.order = ""
    session_state.family = ""
    session_state.genus = ""
    session_state.species = ""
