from pandas import DataFrame
from streamlit import session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
    RANKS,
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
        plants = [
            (taxon, conf["lowest_common_rank_id"])
            for conf in [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH]
            for taxon in conf["taxon"]
        ]
        session_state.plant_to_search = DataFrame(
            plants,
            columns=["taxon", "lowest_common_rank_id"],
        )

    if "insect_to_search" not in session_state:
        insects = [
            (taxon, INSECT_TO_SEARCH["lowest_common_rank_id"])
            for taxon in INSECT_TO_SEARCH["taxon"]
        ]
        session_state.insect_to_search = DataFrame(
            insects,
            columns=["taxon", "lowest_common_rank_id"],
        )


def reset_session() -> None:
    """Reset session_state parameters."""
    session_state.show = False
    session_state.data = None
    session_state.reveal_data = False
    for rank in RANKS:
        session_state[rank] = ""
