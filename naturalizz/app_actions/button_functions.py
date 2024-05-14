from streamlit import session_state

from naturalizz.app_actions.session import reset_session
from naturalizz.configuration import RANKS
from naturalizz.data_retrieval import (
    clear_cache_data_func,
    random_taxon,
    retrieve_taxon_data,
)


def quizz_starter() -> None:
    """Reset sessions_state parameters and retrieve taxon data."""
    reset_session()
    clear_cache_data_func()
    session_state.show = not session_state.show
    random_taxon_data = random_taxon(taxon_type=session_state.config_choice)
    session_state.data = retrieve_taxon_data(random_taxon_data)


def fill_text_field_with_data() -> None:
    """Fill text field that will be displayed with taxon data."""
    session_state.update(
        {
            key: f"**{value}**: {session_state.data.get(key, '')}"
            for key, value in RANKS.items()
        },
    )
    session_state.reveal_data = True
