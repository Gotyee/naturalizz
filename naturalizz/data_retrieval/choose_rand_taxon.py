from random import choice

from naturalizz.configuration import INSECT_LIST


def random_taxon(taxon: list = INSECT_LIST) -> str:
    return choice(taxon)
