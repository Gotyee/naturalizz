from random import choice

from streamlit import cache_data, session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
    generate_df_from_taxon_config,
)


@cache_data(show_spinner=False)
def _random_insect_taxon() -> dict:
    """Select a random insect taxon from a predefined list."""
    insects_psossbilities = session_state.insect_to_search.copy()
    if insects_psossbilities.empty:
        session_state.insect_to_search = generate_df_from_taxon_config(
            [INSECT_TO_SEARCH],
        )
    chosen_insect = insects_psossbilities.sample(n=1)
    session_state.insect_to_search = insects_psossbilities.drop(chosen_insect.index)
    return chosen_insect.to_dict(orient="records")[0]


@cache_data(show_spinner=False)
def _random_plant_taxon() -> dict:
    """Select a random plant taxon from a predefined list."""
    plant_possibilities = session_state.plant_to_search.copy()
    if plant_possibilities.empty:
        session_state.plant_to_search = generate_df_from_taxon_config(
            [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH],
        )
    chosen_plant = plant_possibilities.sample(n=1)
    session_state.plant_to_search = plant_possibilities.drop(chosen_plant.index)
    return chosen_plant.to_dict(orient="records")[0]


@cache_data(show_spinner=False)
def random_taxon(taxon_type: str = "ALL") -> dict:
    # TODO: INdexCatalogue
    match taxon_type:
        case "Plant":
            return _random_plant_taxon()
        case "Insect":
            return _random_insect_taxon()
        case "ALL":
            return choice([_random_plant_taxon(), _random_insect_taxon()])


def clear_random_cache() -> None:
    random_taxon.clear()
    _random_plant_taxon.clear()
    _random_insect_taxon.clear()
