from __future__ import annotations
from enum import Enum, auto

class Paradigm(Enum):
    NONE = auto()
    KFULIM = auto()
    PE_YOD = auto()  # used only for PAAL
    AYIN_WAW = auto()  # used only for PAAL
    PE_ALEF = auto()  # used only for PAAL
    PAAL_1 = auto()
    PAAL_2 = auto()
    PAAL_3 = auto()
    PAAL_4 = auto()


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
