from random import choice

from streamlit import cache_data

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
)


@cache_data(show_spinner=False)
def _random_insect_taxon() -> dict:
    """Select a random insect taxon from a predefined list."""
    return {
        "taxon": choice(INSECT_TO_SEARCH["taxon_list"]),
        "lowest_common_rank_id": INSECT_TO_SEARCH["lowest_common_rank_id"],
    }


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
