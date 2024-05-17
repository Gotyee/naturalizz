from random import choice

from pandas import DataFrame
from streamlit import cache_data, session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
)


@cache_data(show_spinner=False)
def _random_insect_taxon() -> dict:
    """Select a random insect taxon from a predefined list."""
    insects_psossbilities = session_state.insect_to_search.copy()
    print(len(insects_psossbilities))
    if insects_psossbilities.empty:
        insects_psossbilities = DataFrame(
            [
                (taxon, INSECT_TO_SEARCH["lowest_common_rank_id"])
                for taxon in INSECT_TO_SEARCH["taxon"]
            ],
            columns=["taxon", "lowest_common_rank_id"],
        )
    chosen_insect = insects_psossbilities.sample(n=1)
    session_state.insect_to_search = insects_psossbilities.drop(chosen_insect.index)
    print(len(session_state.insect_to_search))
    return chosen_insect.to_dict(orient="records")[0]


@cache_data(show_spinner=False)
def _random_plant_taxon() -> dict:
    """Select a random plant taxon from a predefined list."""
    if choice([True, False]):
        return {
            "taxon": choice(PLANTS_SPECIES_TO_SEARCH["taxon_list"]),
            "lowest_common_rank_id": PLANTS_SPECIES_TO_SEARCH["lowest_common_rank_id"],
        }
    return {
        "taxon": choice(PLANTS_FAMILIES),
        "rank_filter": ["family"],
    }


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
