from __future__ import annotations
from enum import Enum, auto


class Paradigm(Enum):
    NONE = auto()
    KFULIM = auto()
    KFULIM_2 = auto()  # used only for HUFAL
    NO_PREFIX = auto()  # used for words like 'hUnDA!s', 'hU_wA!n', 'nI_sa!H', 'nI_qa!H'
    PE_ALEF = auto()  # used only for PAAL
    PAAL_1 = auto()
    PAAL_2 = auto()
    PAAL_3 = auto()  # some of the verbs that start with "[QRhj]"
    PAAL_4 = auto()
    PAAL_5 = auto()  # some of the verbs that end with "a!Q"

    def is_kfulim(self) -> bool:
        return self in (Paradigm.KFULIM, Paradigm.KFULIM_2)

    def is_paal(self) -> bool:
        return self in (
            Paradigm.PE_ALEF,
            Paradigm.PAAL_1,
            Paradigm.PAAL_2,
            Paradigm.PAAL_3,
            Paradigm.PAAL_4,
            Paradigm.PAAL_5,
        )


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
