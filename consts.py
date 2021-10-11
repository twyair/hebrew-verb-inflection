from __future__ import annotations
from enum import Enum, auto

class Binyan(Enum):
    PAAL = auto()
    PIEL = auto()
    PUAL = auto()
    NIFAL = auto()
    HIFIL = auto()
    HUFAL = auto()
    HITPAEL = auto()


class Pronoun(Enum):
    ANI = auto()
    ATA = auto()
    AT = auto()
    HU = auto()
    HI = auto()
    ANACNU = auto()
    ATEM = auto()
    ATEN = auto()
    HEM = auto()
    HEN = auto()


# TODO: rename
class Present(Enum):
    MALE_SINGULAR = auto()
    MALE_PLURAL = auto()
    FEMALE_SINGULAR = auto()
    FEMALE_PLURAL = auto()
