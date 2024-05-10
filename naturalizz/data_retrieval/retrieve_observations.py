from random import choice

from pyinaturalist import Taxon
from pyinaturalist.v1.taxa import get_taxa, get_taxa_by_id
from streamlit import cache_data


def _random_taxon_photo(ancestors: list[Taxon], taxon_id: int):
    """Retrieve all images related to a taxon and returns one randomly"""
    taxon_photos = next(
        (ancest.taxon_photos for ancest in ancestors if ancest.id == taxon_id), None
    )
    return choice(taxon_photos)


@cache_data
def _retrieve_taxon_and_ancestors(
    taxon_name: str, rank_filter: str | list[str], page: int, per_page: int
):
    taxon_api = get_taxa(
        q=taxon_name, rank=rank_filter, locale="fr", page=page, per_page=per_page
    )
    if taxon_api["total_results"] == 0:
        raise ValueError(f"There was an issue for {taxon_name}")

    taxon = Taxon.from_json_list(taxon_api)[0]
    ancestors_api = get_taxa_by_id(taxon.ancestor_ids, locale="fr")
    ancestors = Taxon.from_json_list(ancestors_api)
    return taxon, ancestors


def retrieve_taxon_data(
    taxon_name, rank_filter=["genus", "species"], page=1, per_page=1
):
    print(taxon_name)
    taxon, ancestors = _retrieve_taxon_and_ancestors(
        taxon_name=taxon_name, rank_filter=rank_filter, page=page, per_page=per_page
    )

    return {
        "name": taxon.preferred_common_name,
        "photo": _random_taxon_photo(ancestors=ancestors, taxon_id=taxon.id),
        **_get_rank_data(ancestors),
    }


def _get_rank_data(ancestors: list[Taxon]):
    """Retrieve rank name for each ancestor"""
    ranks = {"order", "class", "family", "genus", "species"}
    rank_dict = {rank: "" for rank in ranks}
    return {
        ancestor.rank: ancestor.full_name
        for ancestor in ancestors
        if ancestor.rank in rank_dict
    }
