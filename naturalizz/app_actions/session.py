from pandas import DataFrame, concat
from streamlit import session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
    PYRENEAN_FAMILIES_TO_SEARCH,
    PYRENEAN_SPECIES_TO_SEARCH,
    RANKS,
    TAXON_TYPE,
    generate_df_from_taxon_config,
)


def init_session() -> None:
    """Init session_state parameters."""
    if "data" not in session_state:
        session_state.data = None

    if "reveal_data" not in session_state:
        session_state.reveal_data = False

    if "ready_to_restart" not in session_state:
        session_state.ready_to_restart = True

    for rank in RANKS:
        if rank not in session_state:
            session_state[rank] = ""

    if "config_choice" not in session_state:
        session_state.config_choice = "ALL"

    if "answer_data" not in session_state:
        session_state.answer_data = DataFrame()

    if TAXON_TYPE["plant"] not in session_state:
        session_state[TAXON_TYPE["plant"]] = generate_df_from_taxon_config(
            [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH],
        )

    if TAXON_TYPE["insect"] not in session_state:
        session_state[TAXON_TYPE["insect"]] = generate_df_from_taxon_config(
            [INSECT_TO_SEARCH],
        )

    if TAXON_TYPE["pyrenean"] not in session_state:
        session_state[TAXON_TYPE["pyrenean"]] = generate_df_from_taxon_config(
            [PYRENEAN_FAMILIES_TO_SEARCH, PYRENEAN_SPECIES_TO_SEARCH],
        )


def reset_session() -> None:
    """Reset session_state parameters."""
    session_state.data = None
    session_state.reveal_data = False
    for rank in RANKS:
        session_state[rank] = ""


def store_answers_state() -> None:
    """Append taxon data to a df with answer state."""
    data_for_df = {key: session_state.data[key] for key in RANKS}
    if session_state.answer == "Correct":
        session_state.answer_data = concat(
            [
                session_state.answer_data,
                DataFrame([data_for_df]).assign(answer=True),
            ],
            ignore_index=True,
        )
    elif session_state.answer == "Wrong":
        session_state.answer_data = concat(
            [
                session_state.answer_data,
                DataFrame([data_for_df]).assign(answer=False),
            ],
            ignore_index=True,
        )
    session_state.answer = None
