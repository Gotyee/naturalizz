from random import sample
from re import escape

from pandas import DataFrame
from pyinaturalist import Observation, Taxon
from pyinaturalist.v1.observations import get_observations
from pyinaturalist.v1.taxa import get_taxa, get_taxa_by_id
from pyinaturalist_convert import to_dataframe
from streamlit import cache_data
from unidecode import unidecode

from naturalizz.configuration import NB_PIC_DISPLAYED, RANKS

# TODO: Optimize func


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
    rank_filter = taxon_search_data["rank_filter"] or ["genus", "species"]
    lowest_common_rank_id = taxon_search_data["lowest_common_rank_id"] or [
        "genus",
        "species",
    ]
    lowest_common_rank_id = taxon_search_data.get("lowest_common_rank_id")
    taxons = get_taxons(
        taxon_name=taxon_name,
        rank_filter=rank_filter,
        page=page,
        per_page=per_page,
    )
    if "family" not in rank_filter:  # no need for filtering in that case
        taxons = _filter_alias_names(taxons=taxons, taxon_name=taxon_name)
    if lowest_common_rank_id:
        taxons = _filter_ancestors(
            taxons=taxons,
            lowest_common_rank_id=lowest_common_rank_id,
        )
    taxon = taxons.sample(n=1)
    taxon_dict = taxon.to_dict(orient="records")[0]

    return {
        "name": taxon_dict["preferred_common_name"] or taxon_dict["name"],
        "photo": _random_taxon_photo(taxon_dict["id"]),
        **_get_rank_data(get_taxon_ancestors(taxon_dict["ancestor_ids"])),
    }


def get_taxon_ancestors(ancestor_ids: tuple) -> list[Taxon]:
    """Retrieve all ancestors for a taxon."""
    return to_dataframe(Taxon.from_json_list(get_taxa_by_id(ancestor_ids, locale="fr")))


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
    if "family" in rank_filter:
        # retrieving a random specie from this particular family
        taxons = Taxon.from_json_list(
            get_taxa(
                rank=["species"],
                taxon_id=taxons[0].id,
                locale="fr",
                preferred_place_id=6753,
                page=page,
                per_page=per_page,
            ),
        )
    if not taxons:
        msg = f"There was an issue for {taxon_name}"
        raise ValueError(msg)
    return to_dataframe(taxons)


def _get_obs_from_taxon(taxon_id: int) -> list[Observation]:
    """Retrieve observations for a specific taxon with a preference for certain parameters."""
    params_list = [
        {
            "taxon_id": taxon_id,
            "photos": True,
            "place_id": 6753,
            "quality_grade": "research",
            "term_id": 1,
            "term_value_id": 2,
        },
        {
            "taxon_id": taxon_id,
            "photos": True,
            "quality_grade": "research",
            "place_id": 6753,
        },
        {"taxon_id": taxon_id, "photos": True, "quality_grade": "research"},
    ]

    # Create tasks for each set of parameters
    for params in params_list:
        obs = Observation.from_json_list(get_observations(**params, per_page=100))
        if obs:
            print(params)
            print(len(obs))
            return obs
    return []


@cache_data(show_spinner=False)
def _random_taxon_photo(
    taxon_id: int,
    nb_photos: int = NB_PIC_DISPLAYED,
) -> list[str]:
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


def _get_rank_data(ancestors: DataFrame) -> dict:
    """Retrieve rank name for each ancestor."""
    ancestors = ancestors[ancestors["rank"].isin(RANKS.keys())].copy()
    ancestors.loc[:, "rank_label"] = ancestors["name"].str.cat(
        ancestors["preferred_common_name"].fillna(""),
        sep=" - ",
    )
    return ancestors.set_index("rank")["rank_label"].to_dict()


def _filter_alias_names(taxons: list[Taxon], taxon_name: str) -> DataFrame:
    """Filter to avoid unwanted match from api.

    For instance 'Puceron' is matched with Chrysopa Perla by the api,
    because one alias of this specie is 'Lion des Pucerons'
    """
    if len(taxons) == 1:
        return taxons

    pattern = rf"\b{escape(unidecode(taxon_name).lower())}\b"
    taxons["name_for_filter"] = (
        taxons["name"].str.lower() + " " + taxons["preferred_common_name"].str.lower()
    ).apply(unidecode)
    df_taxons = taxons[taxons["name_for_filter"].str.contains(pattern)]
    if df_taxons.empty:
        msg = f"Issue filtering alias names for {taxon_name}"
        raise ValueError(msg)
    return df_taxons


def _filter_ancestors(taxons: DataFrame, lowest_common_rank_id: str) -> DataFrame:
    """Manually removes taxons with undesired ancestors. (Poisson-guêpe example)."""
    df_taxon = taxons[taxons["ancestor_ids"].map(lambda x: lowest_common_rank_id in x)]
    if df_taxon.empty:
        msg = f"Issue while filtering ancestors with this ID {lowest_common_rank_id}"
        raise ValueError(msg)
    return df_taxon
