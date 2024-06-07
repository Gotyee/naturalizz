import logging

from pandas import DataFrame, concat
from pyinaturalist import Taxon
from pyinaturalist.v1.taxa import get_taxa, get_taxa_by_id
from pyinaturalist_convert import to_dataframe

from naturalizz.configuration import RANKS

logger = logging.getLogger(__name__)


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
    taxons = get_taxons(
        taxon_name=taxon_name,
        rank_filter=rank_filter,
        page=page,
        per_page=per_page,
    )
    if lowest_common_rank_id:
        taxons = _filter_ancestors(
            taxons=taxons,
            lowest_common_rank_id=lowest_common_rank_id,
        )

    taxons["taxon_name_for_search"] = taxon_name
    taxons["rank_filter"] = [rank_filter] * len(
        taxons,
    )  # TODO: better storage for metadata

    ancestors_data = _retrieve_ancestors_data(
        list(taxons["ancestor_ids"]),
    )
    ancestors_data.to_parquet("ancestors_data.parquet")
    logger.info("Extracted ancestors_data")
    taxons[["id", "preferred_common_name", "name", "wikipedia_url"]].to_parquet(
        "taxons_data.parquet",
    )
    logger.info("Extracted taxons_data")
    return


def get_taxons(
    taxon_name: str,
    rank_filter: str | list[str],
    page: int,
    per_page: int,
) -> DataFrame:
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
    if rank_filter != ["genus", "species"]:
        # retrieving a random specie from this higher taxon
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
        msg = f"No Taxon found with iNaturalist aPI for {taxon_name}"
        raise ValueError(msg)
    return to_dataframe(taxons)


def _retrieve_ancestors_data(ancestor_ids: list) -> DataFrame:
    """Retrieve data for each list of ancestors."""
    ancestors_data = DataFrame()
    for ancestor_list in ancestor_ids:
        ancestors = _get_taxon_ancestors(ancestor_list)
        ancestors = ancestors[ancestors["rank"].isin(RANKS.keys())].copy()
        ancestors_data = concat(
            [ancestors_data, ancestors[["id", "name", "preferred_common_name"]]],
        )
    return ancestors_data.drop_duplicates("id")


def _get_taxon_ancestors(ancestor_ids: tuple) -> list[Taxon]:
    """Retrieve all ancestors for a taxon."""
    return to_dataframe(Taxon.from_json_list(get_taxa_by_id(ancestor_ids, locale="fr")))


def _filter_ancestors(taxons: DataFrame, lowest_common_rank_id: str) -> DataFrame:
    """Manually removes taxons with undesired ancestors. (Poisson-guêpe example)."""
    df_taxon = taxons[taxons["ancestor_ids"].map(lambda x: lowest_common_rank_id in x)]
    if df_taxon.empty:
        msg = f"Issue while filtering ancestors with this ID {lowest_common_rank_id}"
        raise ValueError(msg)
    return df_taxon


retrieve_taxon_data(
    {"taxon": "Aeschne", "lowest_common_rank_id": 372739, "rank_filter": None},
)
