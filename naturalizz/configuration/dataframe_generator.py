from pandas import DataFrame


def generate_df_from_taxon_config(configurations: list) -> DataFrame:
    """Generate a dataframe with each taxon and its param as a row."""
    config_list_flat = [
        (
            taxon,
            taxon_config.get("lowest_common_rank_id"),
            taxon_config.get("rank_filter"),
        )
        for taxon_config in configurations
        for taxon in taxon_config["taxon"]
    ]
    return DataFrame(
        config_list_flat,
        columns=["taxon", "lowest_common_rank_id", "rank_filter"],
        dtype=object,
    )
