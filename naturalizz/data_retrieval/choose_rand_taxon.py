from random import choice

from streamlit import cache_data, session_state

from naturalizz.configuration import (
    INSECT_TO_SEARCH,
    PLANTS_FAMILIES,
    PLANTS_SPECIES_TO_SEARCH,
    TAXON_TYPE,
    generate_df_from_taxon_config,
)


@cache_data(show_spinner=False)
def _random_taxon_core(taxon_type: str, taxon_to_search: list):
    taxon_possibilities = session_state[taxon_type].copy()
    if taxon_possibilities.empty:
        session_state[taxon_type] = generate_df_from_taxon_config(taxon_to_search)
    chosen_taxon = taxon_possibilities.sample(n=1)
    session_state[taxon_type] = taxon_possibilities.drop(chosen_taxon.index)
    return chosen_taxon.to_dict(orient="records")[0]


@cache_data(show_spinner=False)
def random_taxon(taxon_type: str = TAXON_TYPE["all"]) -> dict:
    """Return random taxon among all or selected possibilities."""
    if taxon_type == TAXON_TYPE["plant"]:
        return _random_taxon_core(
            TAXON_TYPE["plant"],
            [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH],
        )
    if taxon_type == TAXON_TYPE["insect"]:
        return _random_taxon_core(TAXON_TYPE["insect"], [INSECT_TO_SEARCH])
    return choice(
        [
            _random_taxon_core(
                TAXON_TYPE["plant"],
                [PLANTS_FAMILIES, PLANTS_SPECIES_TO_SEARCH],
            ),
            _random_taxon_core(TAXON_TYPE["insect"], [INSECT_TO_SEARCH]),
        ],
    )


def clear_random_cache() -> None:
    random_taxon.clear()
    _random_taxon_core.clear()
