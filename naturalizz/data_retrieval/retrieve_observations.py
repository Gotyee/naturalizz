from random import choice

from pyinaturalist import Observation, Taxon
from pyinaturalist.v1.observations import get_observations
from pyinaturalist.v1.taxa import get_taxa, get_taxa_by_id


def retrieve_observations(taxon_name, page=10, per_page=20):
    # ! Deprecated , do not use
    obs_api = get_observations(
        taxon_name=taxon_name,
        photos=True,
        page=page,
        per_page=per_page,
    )
    if not obs_api:
        raise (f"There was an issue for {taxon_name}")
    observations = Observation.from_json_list(obs_api)
    unique_observation = choice(observations)
    return {
        "name": unique_observation.taxon.full_name,
        "photo": unique_observation.photos[0],
    }


def retrieve_taxon_data(
    taxon_name, rank_filter=["genus", "species"], page=1, per_page=1
):
    taxon_api = get_taxa(
        q=taxon_name, rank=rank_filter, locale="fr", page=page, per_page=per_page
    )
    if not taxon_api:
        raise (f"There was an issue for {taxon_name}")
    print(taxon_name)
    taxon = Taxon.from_json_list(taxon_api)[0]
    ancestors_api = get_taxa_by_id(taxon.ancestor_ids, locale="fr")
    ancestors = Taxon.from_json_list(ancestors_api)
    taxon_photos = next(
        (ancest.taxon_photos for ancest in ancestors if ancest.id == taxon.id), None
    )

    return {
        "name": taxon.preferred_common_name,
        "photo": choice(taxon_photos),
        "order": next(
            (ancest.full_name for ancest in ancestors if ancest.rank == "order"),
            "",
        ),
        "class": next(
            (ancest.full_name for ancest in ancestors if ancest.rank == "class"),
            "",
        ),
        "family": next(
            (ancest.full_name for ancest in ancestors if ancest.rank == "family"),
            "",
        ),
        "genus": next(
            (ancest.full_name for ancest in ancestors if ancest.rank == "genus"),
            "",
        ),
        "species": next(
            (ancest.full_name for ancest in ancestors if ancest.rank == "species"),
            "",
        ),
    }
