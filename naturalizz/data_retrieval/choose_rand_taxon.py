from random import choice

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
)


def _random_insect_taxon() -> dict:
    """Select a random insect taxon from a predefined list."""
    return {
        "taxon": choice(INSECT_TO_SEARCH["taxon_list"]),
        "lowest_common_rank_id": INSECT_TO_SEARCH["lowest_common_rank_id"],
        "rank_filter": ["genus", "species"],
    }


def _random_plant_taxon() -> dict:
    """Select a random plant taxon from a predefined list."""
    if choice([True, False]):
        return {
            "taxon": choice(PLANTS_SPECIES_TO_SEARCH["taxon_list"]),
            "lowest_common_rank_id": PLANTS_SPECIES_TO_SEARCH["lowest_common_rank_id"],
            "rank_filter": ["genus", "species"],
        }
    return {
        "taxon": choice(PLANTS_FAMILIES),
        "rank_filter": ["family"],
    }


def random_taxon(taxon_type: str = "ALL") -> dict:
    # TODO: INdexCatalogue
    match taxon_type:
        case "Plant":
            return _random_plant_taxon()
        case "Insect":
            return _random_insect_taxon()
        case "ALL":
            return choice([_random_plant_taxon(), _random_insect_taxon()])
