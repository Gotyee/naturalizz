from streamlit import session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
    RANKS,
    generate_df_from_taxon_config,
)


def init_session() -> None:
    """Init session_state parameters."""
    if "show" not in session_state:
        session_state.show = False

    if "data" not in session_state:
        session_state.data = None

    if "reveal_data" not in session_state:
        session_state.reveal_data = False

    for rank in RANKS:
        if rank not in session_state:
            session_state[rank] = ""

    if "config_choice" not in session_state:
        session_state.config_choice = "ALL"

    if "plant_to_search" not in session_state:
        session_state.plant_to_search = generate_df_from_taxon_config(
            [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH],
        )

    if "insect_to_search" not in session_state:
        session_state.insect_to_search = generate_df_from_taxon_config(
            [INSECT_TO_SEARCH],
        )


def reset_session() -> None:
    """Reset session_state parameters."""
    session_state.show = False
    session_state.data = None
    session_state.reveal_data = False
    for rank in RANKS:
        session_state[rank] = ""
