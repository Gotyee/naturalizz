from random import choice, sample
from re import escape, search

from pyinaturalist import Observation, Taxon
from pyinaturalist.v1.observations import get_observations
from pyinaturalist.v1.taxa import get_taxa, get_taxa_by_id
from streamlit import cache_data
from unidecode import unidecode

from naturalizz.configuration import NB_PIC_DISPLAYED, RANKS


def clear_cache_data_func() -> None:
    """Clear cache for required function."""
    retrieve_taxon_data.clear()
    _random_taxon_photo.clear()


@cache_data(show_spinner=False)
def retrieve_taxon_data(
    taxon_search_data: dict,
    page: int = 1,
    per_page: int = 30,
) -> dict:
    """Retrieve taxon data from inaturlist.

    Parameters
    ----------
    taxon_search_data : dict
        Contains parameter for API call such as
            - taxon_name
            - rank_filter
            - lowest_common_rank_id
    page : int
        Number of results page
    per_page : int
        Number of results per page

    Returns
    -------
    dict
        data related to the taxon

    """
    taxon_name = taxon_search_data["taxon"]
    rank_filter = taxon_search_data.get("rank_filter", ["genus", "species"])
    lowest_common_rank_id = taxon_search_data.get("lowest_common_rank_id")
    taxons = get_taxons(
        taxon_name=taxon_name,
        rank_filter=rank_filter,
        page=page,
        per_page=per_page,
    )
    taxons = _filter_alias_names(taxons=taxons, taxon_name=taxon_name)
    if lowest_common_rank_id:
        taxons = _filter_ancestors(
            taxons=taxons,
            lowest_common_rank_id=lowest_common_rank_id,
        )
    taxon = choice(taxons)
    ancestors = get_taxon_ancestors(ancestor_ids=tuple(taxon.ancestor_ids))

    return {
        "name": taxon.preferred_common_name,  # TODO: check if name is empty
        "photo": _random_taxon_photo(taxon_id=taxon.id),
        **_get_rank_data(ancestors),
    }


@cache_data(show_spinner=False)
def get_taxons(
    taxon_name: str,
    rank_filter: str | list[str],
    page: int,
    per_page: int,
) -> list[Taxon]:
    """Retrieve taxa data for a given string."""
    taxons = Taxon.from_json_list(
        get_taxa(
            q=taxon_name,
            rank=rank_filter,
            locale="fr",
            preferred_place_id=6753,
            page=page,
            per_page=per_page,
        ),
    )
    if not taxons:
        msg = f"There was an issue for {taxon_name}"
        raise ValueError(msg)
    return taxons


@cache_data(show_spinner=False)
def get_taxon_ancestors(ancestor_ids: tuple) -> list[Taxon]:
    """Retrieve all ancestors for a taxon."""
    return Taxon.from_json_list(get_taxa_by_id(ancestor_ids, locale="fr"))


@cache_data(show_spinner=False)
def _get_obs_from_taxon(taxon_id: int) -> list[Observation]:
    """Retrieve observations for a specifi taxon.

    Filtering to keep only obs with Life Stage = Adult.
    """
    obs = Observation.from_json_list(
        get_observations(
            taxon_id=taxon_id,
            photos=True,
            place_id=6753,  # France
            quality_grade="research",
            term_id=1,
            term_value_id=2,
        ),
    )
    if not obs:
        obs = Observation.from_json_list(
            get_observations(
                taxon_id=taxon_id,
                photos=True,
                quality_grade="research",
                place_id=6753,
            ),
        )
    if not obs:
        obs = Observation.from_json_list(
            get_observations(
                taxon_id=taxon_id,
                photos=True,
                quality_grade="research",
            ),
        )  # TODO :possible to get this info in one API call?

    return obs


@cache_data(show_spinner=False)
def _random_taxon_photo(taxon_id: int, nb_photos: int = NB_PIC_DISPLAYED) -> Taxon:
    """Retrieve all images related to a taxon and returns three randomly."""
    taxon_obs = _get_obs_from_taxon(taxon_id)
    taxon_photos = [pic for obs in taxon_obs for pic in obs.photos]
    if not taxon_photos:
        msg = f"No picture for taxon ID {taxon_id}"
        raise ValueError(msg)
    if len(taxon_photos) < nb_photos:
        taxon_photos.extend([None] * (nb_photos - len(taxon_photos)))
        return taxon_photos
    return sample(taxon_photos, nb_photos)


def _get_rank_data(ancestors: list[Taxon]) -> dict:
    """Retrieve rank name for each ancestor."""
    ranks = RANKS.keys()
    rank_dict = {rank: "" for rank in ranks}
    return {
        ancestor.rank: f"{ancestor.name} ({ancestor.preferred_common_name})"
        if ancestor.preferred_common_name
        else f"{ancestor.name}"
        for ancestor in ancestors
        if ancestor.rank in rank_dict
    }


def _filter_alias_names(taxons: list[Taxon], taxon_name: str) -> list[Taxon]:
    """Filter to avoid unwanted match from api.

    For instance 'Puceron' is matched with Chrysopa Perla by the api,
    because one alias of this specie is 'Lion des Pucerons'
    """
    if len(taxons) == 1:
        return taxons

    pattern = rf"\b{escape(unidecode(taxon_name).lower())}\b"
    filtered_list = [
        taxon
        for taxon in taxons
        if search(
            pattern,
            unidecode(
                f"{taxon.name.lower()} {taxon.preferred_common_name.lower()}",
            ),
        )
    ]
    if not filtered_list:
        msg = f"Issue filtering alias names for {taxon_name}"
        raise ValueError(msg)
    return filtered_list


def _filter_ancestors(taxons: list[Taxon], lowest_common_rank_id: str) -> list[Taxon]:
    """Remove manually taxons with undesired ancestors."""
    taxons_with_proper_ancest = [
        taxon for taxon in taxons if lowest_common_rank_id in taxon.ancestor_ids
    ]
    if not taxons_with_proper_ancest:
        msg = f"Issue while filtering ancestors with this ID {lowest_common_rank_id}"
        raise ValueError(msg)
    return taxons_with_proper_ancest
