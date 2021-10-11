from __future__ import annotations
from enum import Enum, auto
import re
from typing import Optional

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

    @staticmethod
    def new(verb: str, binyan: Binyan, root: str) -> Paradigm:
        if verb in PE_ALEF:
            return Paradigm.PE_ALEF
        if verb in PAAL_4:
            return Paradigm.PAAL_4
        if verb in PAAL_3:
            return Paradigm.PAAL_3
        if verb in PAAL_1:
            return Paradigm.PAAL_1
        if verb in PAAL_2:
            return Paradigm.PAAL_2
        if binyan == Binyan.PAAL and verb.startswith("y"):
            return Paradigm.PE_YOD
        if len(root) == 3 and root[1] == root[2]:
            return Paradigm.KFULIM
        if binyan == Binyan.PAAL and len(root) == 3 and root[1] == "w":
            return Paradigm.AYIN_WAW
        return Paradigm.NONE

CONSONANTS = tuple("QbvgGdDhwzj7ykxlmnsRpfZqrcStT")
GRONIYOT = tuple("hjQR")
VOWELS = tuple("aiueoAIUEOWÁáéó")
PRONOUN_FUTURE_PREFIX = {
    Pronoun.ANI: "Q",
    Pronoun.ATA: "T",
    Pronoun.AT: "T",
    Pronoun.HU: "y",
    Pronoun.HI: "T",
    Pronoun.ANACNU: "n",
    Pronoun.ATEM: "T",
    Pronoun.ATEN: "T",
    Pronoun.HEM: "y",
    Pronoun.HEN: "T",
}
PE_ALEF = {'QahA!v', 'Qafa!H', 'QahA!d', 'QajA!z', 'QamA!r', 'QaxA!l', 'QavA!d', 'Qava!H', }
PAAL_1 = {
    'RavA!c', 'QavA!d', 'caQA!7', 'QasA!f', 'hawa!H', 'nagA!f', 'baSA!m', 'halA!x', 'lahA!v', 'TaQA!m', 'ca!r', 'saRA!d', 'lajA!Z', 'maja!Q', 'QasA!r', 'caxA!n', 'ZajA!q', 'QahA!v', 'qa!Q', 'QarA!v', 'ZanA!n', 'macA!c', 'Sane!Q', 'naqA!m', 'caxA!v', 'lahA!g', 'Zame!Q', 'ZaRA!f', 'GaRA!c', 'paRA!l', 'nasA!R', 'yaqA!d', 'saxA!l', 'Qana!H', 'yaRA!f', 'male!Q', 'qarA!n', 'la!Z', 'DaQA!g', 'sajA!v', 'ja!l', 'jara!H', 'bajA!l', 'rajA!f', 'maRA!x', '7aRA!n', 'zaqA!n', 'qamA!l', 'ZaRA!n', 'caQA!l', 'kajA!l', 'baRA!l', 'QagA!f', 'Qara!H', 'nacA!v', 'yasA!d', 'natA!Z', 'me!t', 'raqA!v', 'GaQA!l', 'nasA!x', 'ra!c', 'qarA!v', '7ahA!r', 'natA!c', 'bara!Q', 'camA!n', 'jamA!Z', 'kavA!d', 'caxA!x', 'GahA!r', 'rajA!q', 'jazA!q', 'pajA!t', 'na7A!r', 'DajA!q', 'jafa!H', 'jarA!d', 'zahA!r', 'na7A!f', 'RacA!t', 'paRA!m', 'yaRA!Z', 'na7a!H', 'lA!R', 'bahA!q', 'ragA!l', 'Daca!Q', 'QarA!g', 'ca!t', 'haga!H', 'kacA!l', 'RacA!r', 'yavA!c', 'barA!d', 'navA!l', 'GaRA!l', 'qarA!m', 'Zava!Q', 'QaZA!l', 'Gama!Q', 'QagA!r', 'DavA!q', 'GavA!r', 'yare!Q', 'qacA!c', 'GahA!q', 'yarA!c', 'SagA!v', 'caRA!7', 'jasa!H', 'qarA!c', 'natA!z', 'caQA!f', '7ajA!n', 'rA!v', 'pajA!r', 'yacA!n', 'QamA!d', 'nafA!j', 'yaRA!d', 'QarA!z', 'DahA!r', 'sa!d', 'cajA!q', 'jaZa!H', 'qadA!r', 'naZA!r', 'QazA!r', 'nafA!l', 'ZaRA!d', 'rahA!v', 'laRA!7', 'pacA!r', 'lavA!c', 'naRA!l', 'majA!l', 'DA!q', 'pahA!q', 'sajA!r', 'nadA!r', 'GajA!x', 'DalA!q', 'ba7A!l', 'zaRA!m', '7ala!Q', 'cA!j', 'sava!Q', 'naRA!r', 'yada!H', 'caQA!g', 'QanA!q', 'caQA!v', 'yaqA!v', 'raRA!d', 'ha!m', 'QamA!r', 'naca!H', 'jasA!r', 'jada!H', 'ravA!Z', 'GadA!l', 'yara!H', 'calA!m', 'maRA!d', 'RA!z', 'nagA!h', 'maRA!l', 'najA!t', 'yazA!m', 'raQA!m', 'DajA!s', 'Qata!H', 'mA!x', 'jarA!Z', 'nagA!R', 'TaxA!l', 'cafA!r', 'rA!m', 'naSa!Q', 'yafa!H', 'DacA!n', 'janA!n', 'nasA!j', 'yaZa!Q', 'lahA!7', 'qacA!v', 'ba!Q', 'kacA!r', 'rafa!Q', 'yagA!R', 'ZaRA!q', 'SaRA!r', 'najA!r', 'Qala!H', 'laRA!s', 'sajA!f', 'ZahA!l', 'qadA!m', 'RacA!n', 'majA!q', 'QavA!s', 'raRA!v', 'Qava!H', 'nahA!g', 'jarA!v', 'raRA!f', 'majA!Z', 'sama!Q', 'bacA!l', 'QaZA!r', 'jaza!H', 'rA!n', 'bajA!c', 'qa7A!n', 'yaRA!7', 'ZaRA!r', 'raxA!v', 'zaRA!q', 'TajA!m', 'samA!r', 'kaRA!s', 'ZamA!q', 'zaRA!f', 'mahA!l', 'baRA!r', 'nahA!q', 'janA!f', 'yarA!7', 'la!n', 'TaQA!v', 'ra!v', 'laRA!z', 'paRA!r', 'caRA!r', 'QagA!d', 'cafA!l', '7aRA!m', 'naRA!Z', 'TahA!d', 'DaQA!v', 'na7A!R', 'kaQA!v', 'ZahA!v', 'naxA!s', 'rajA!m', 'rahA!7', 'DajA!f', 'DA!l', 'nadA!j', 'rajA!c', 'ja7a!Q', 'zahA!v', 'jawa!H', 'pazA!z', 'nagA!S', 'SajA!q', 'qafa!Q', 'yaZA!r', 'QaxA!l', 'sa!j', 'cajA!d', 'jaca!H', 'nadA!v', 'ra!r', 'saQA!n', 'Qa7A!m', 'barA!x', 'bahA!r', 'hadA!r', 'nagA!v', 'GamA!m', 'QamA!n', 'mahA!r', 'kawA!Z', 'RatA!q', 'kala!Q', 'baZA!q', 'QafA!f', 'paZA!r', 'GajA!n', 'na7A!c', 'ZahA!r', 'TaQA!r', 'cajA!7', 'raRA!m', 'TaQA!w', 'calA!w', 'ratA!t', 'QafA!d', 'baRA!7', 'laqA!q', 'yanA!q', 'yaRa!H', 'saRA!r', 'camA!m', 'sajA!7', 'yaZA!q', 'zajA!l', 'lamA!d', 'Sa!m', 'ragA!c', 'bajA!n', 'QazA!q', 'bajA!r', 'Qafa!H', 'maZa!Q', 'jacA!x', 'lajA!x', 'Sa!S', 'natA!q', 'hada!H', 'nahA!m', 'nazA!r', 'rajA!Z', 'Ga!j', 'naZa!H', 'havA!l', 'baQA!c', 'cajA!f', 'lajA!m', 'laRA!g', 'savA!v', 'GaRA!r', 'caQA!r', 'kajA!c', 'Ga!l', 'ragA!z', 'basA!m', 'yasA!r', 'pajA!s', 'qara!Q', 'TajA!v', 'raRA!c', 'haza!H', 'na7A!l', 'qaZA!r', 'QajA!z', 'ba!n', 'RacA!c', 'QanA!s', 'raRA!Z', 'Qa7A!r', 'baza!Q', 'yarA!q', '7ame!Q', 'hama!H', 'rafA!d', 'maQA!s', 'pajA!d', 'bagA!r', 'caQA!n', 'DaRA!x', 'samA!q', 'natA!n', 'QaxA!f', 'lajA!c', 'najA!l', 'na!r', 'jadA!l', 'GalA!d', 'ZadA!q', 'majA!7', 'QahA!d', 'QafA!Z',
}
# belong to 2+ paal paradigms:
# {'jarA!r', 'DamA!m', 'jaqA!q', 'jafA!f', 'javA!v', 'GadA!d', 'zaqA!q',
# 'hamA!m', 'jaZA!Z', 'malA!l', 'QarA!r', 'ja7A!7', 'jagA!g', 'jacA!c',
# 'kasA!s', 'jaxA!x', }
# {'sa!d', 'la!n', 'ca!r', 'ja!l'}
PAAL_2 = {
    'natA!r', 'TacA!c', 'jalA!d', 'jatA!m', 'jalA!f', 'jarA!7', 'jafA!S', 'jacA!r', 'jata!H', 'ja7A!f', 'jalA!v', 'jafA!t', 'janA!v', 'yadA!R', 'yarA!d', 'jarA!g', 'jamA!d', 'jaqA!r', 'janA!x', 'jalA!c', 'jatA!l', 'jamA!q', 'jazA!r', 'javA!7', 'javA!Z', 'laqA!j', 'nasA!q', 'jacA!v', 'yacA!v', 'jatA!f', 'janA!q', 'jaZA!v', 'nacA!l', 'jacA!d', 'ja7A!v', 'qA!d', 'jafA!z', 'naQA!Z', 'nazA!l', 'jacA!q', 'jaxA!r', 'qA!v', 'jamA!r', 'jarA!f', 'naQA!m', 'jasA!m', 'jatA!x', 'jafA!Z', 'jarA!z', 'haxA!r', 'TA!m', 'jalA!7', 'jatA!r', 'jaSA!x', 'jarA!t', 'jamA!s', 'javA!c', 'jaSA!f', 'jaZA!d', 'jasA!x', 'jalA!Z', 'yalA!d', 'jagA!r', 'jadA!r', 'hadA!x', 'naQA!f', 'javA!l', 'jalA!q', 'naQA!q', 'jasA!l', 'jamA!l', 'jafA!r', 'jala!H', 'Rada!H', 'nacA!q', 'RatA!r',
}
# PAAL_3 = {
#     '7ahA!r', 'jarA!v', 'yavA!c', 'kamA!c', 'RacA!t', 'QacA!m', 'qanA!7', 'calA!w', 'jadA!l', 'RacA!n', 'yaRA!f', 'RacA!c', 'caqA!7', 'DacA!n', 'jarA!d', 'TaQA!w', 'SavA!R', 'cafA!l', 'raRA!v', 'kacA!r', 'baZA!q', 'qarA!v', 'QavA!l', 'bacA!l', 'jafA!Z', 'RarA!v', 'RavA!c', 'QafA!l', 'qamA!l', 'janA!f', 'zaqA!n', 'kajA!c', 'TaQA!v', 'kavA!d', 'ba7A!l', 'camA!n', 'kawA!Z', 'yacA!n', 'jazA!q', 'jamA!Z', 'DavA!q', 'GadA!l', 'calA!m', 'qaZA!r', 'jacA!x', 'jasA!r', 'RatA!q', 'qa7A!n', 'RamA!l', 'QafA!s',
# }
PAAL_3 = {
    'jarA!r', 'DamA!m', 'jaqA!q', 'QacA!r', 'jafA!f', 'QahA!l', 'QafA!l', 'QarA!x', 'javA!v', 'QajA!r', 'GadA!d', 'RaZA!m', 'zaqA!q', 'hamA!m', 'QafA!z', 'jaZA!Z', 'malA!l', 'QarA!r', 'QacA!m', 'ja7A!7', 'QanA!f', 'QarA!j', 'jagA!g', 'jaya!H', 'QalA!f', 'haya!H', 'Sa!j', 'RarA!v', 'jarA!c', 'jacA!c', 'kasA!s', 'QavA!l', 'Sa!j', 'QafA!s', 'jaxA!x', 'ZalA!l', 'QazA!l',
}
PAAL_4 = {
    'cafA!l', 'ba7A!l', 'caqA!7', 'DavA!q', 'yafa!H', 'jacA!x', 'Dawa!H', 'TaQA!w', 'kajA!c', 'naQa!H', 'qanA!7', 'yacA!n', 'kala!H', 'jarA!v', 'yaRA!f', 'RacA!c', 'RacA!t', 'kamA!h', 'qa7A!n', 'bacA!l', 'nawa!H', 'qaca!H', 'TaQA!v', 'jasA!r', 'yagA!R', 'QafA!l', 'Daxa!H', 'yavA!c', 'raza!H', 'kavA!d', 'kava!H', 'zaqA!n', 'RarA!v', 'calA!m', 'jaca!H', 'kawA!Z', 'jamA!Z', 'raRA!v', 'QavA!l', 'RatA!q', 'TamA!h', 'kamA!c', 'jadA!l', 'RacA!n', 'kacA!r', 'rawa!H', 'RamA!l', 'QafA!s', 'Rava!H', 'SamA!j', 'bala!H', 'qarA!v', 'jafA!Z', 'jarA!d', 'hara!H', 'SavA!R', 'RavA!c', 'baZA!q', 'QacA!m', 'cawa!H', 'jazA!q', 'DacA!n', 'Zava!H', 'janA!f', 'GadA!l', 'qamA!l', '7ahA!r', 'qaZA!r', 'camA!n', 'laha!H', 'rafa!H',
} # | {'TA!m', }
PAAL_1 -= PAAL_4
assert not (PAAL_1 & PAAL_2)

DAGESH_LENE = {
    "x": "k",
    "g": "G",
    "t": "T",
    "d": "D",
    "v": "b",
    "f": "p",
}
DAGESH_LENE_REV = {
    "k": "x",
    "G": "g",
    "T": "t",
    "D": "d",
    "b": "v",
    "p": "f",
}
PRONOUN_PAST_SUFFIX = {
    Pronoun.ANI: "Ti",
    Pronoun.ATA: "Ta",
    Pronoun.AT: "T",
    Pronoun.HU: "",
    Pronoun.HI: "a!H",
    Pronoun.ANACNU: "nu",
    Pronoun.ATEM: "TE!m",
    Pronoun.ATEN: "TE!n",
    Pronoun.HEM: "u!",
    Pronoun.HEN: "u!",
}
PRESENT_SUFFIX = {
    Present.FEMALE_SINGULAR: "a!H",
    Present.MALE_PLURAL: "i!m",
    Present.FEMALE_PLURAL: "W!t"
}

def add_dagesh_lene(c: str) -> str:
    return DAGESH_LENE.get(c, c)

def remove_dagesh_lene(c: str) -> str:
    return DAGESH_LENE_REV.get(c, c)

def add_dagesh_forte(c: str) -> str:
    if c in "RQjhr":
        return c
    else:
        return "_" + add_dagesh_lene(c)

def fixup(word: str) -> str:
    return re.sub(r"(.)\1", r"\1%\1", word).replace("%", "3")

def inflect_future(base: str, binyan: Binyan, pronoun: Pronoun, paradigm: Paradigm) -> str:
    if binyan in (Binyan.HITPAEL, Binyan.PIEL, Binyan.PUAL):
        assert base.startswith("yI") and binyan == Binyan.HITPAEL or base.startswith(
            "y3") and binyan != Binyan.HITPAEL
        base = base[1:]

        base_at = re.sub(r"[Á]", "", base)
        if base_at.endswith("E!H"):
            base_at = base_at[:-3]
        else:
            assert base_at.endswith(CONSONANTS)
            if re.search("á..!", base_at):
                base_at = re.sub("á(.).!", r"A\1", base_at)
            else:
                base_at = base_at[:-3] + ("á" if base_at[-4] in GRONIYOT else "3") + base_at[-1]

        if pronoun == Pronoun.ANI:
            return "Q" + ("E" if base.startswith("I") else "á") + base[1:]
        if pronoun in (Pronoun.ATA, Pronoun.HI):
            return "T" + base
        if pronoun == Pronoun.AT:
            return "T" + base_at + "i!"
        if pronoun == Pronoun.HU:
            return "y" + base
        if pronoun == Pronoun.ANACNU:
            return "n" + base
        if pronoun == Pronoun.ATEM:
            return "T" + base_at + "u!"
        if pronoun in (Pronoun.ATEN, Pronoun.HEN):
            base = "T" + base.replace("Á", "")
            if base.endswith("n"):
                return base[:-1] + "_naH"
            elif base.endswith("E!H"):
                return base[:-3] + "E!YnaH"
            elif re.search(r"e![jhR]$", base):
                return base.replace("e!", "A!") + "naH"
            elif re.search(r".!Q$", base):
                return re.sub(".!", "E!", base) + "naH"
            return base + ("3" if base[-3] in "aiueoWY" else "") + "naH"
        if pronoun == Pronoun.HEM:
            return "y" + base_at + "u!"
    elif binyan == Binyan.HIFIL:
        base = PRONOUN_FUTURE_PREFIX[pronoun] + base[1:]

        base_at = base.replace("Á", "")
        if base_at.endswith("E!H"):
            base_at = base_at[:-3]
        elif Paradigm.KFULIM == paradigm and base_at[-1] not in "jhQRr" and not re.search(r"(.).!\1$", re.sub("[fvxdgt]$", lambda m: add_dagesh_lene(m[0]), base_at)):
            base_at = base_at[:-1] + "_" + add_dagesh_lene(base_at[-1])
        else:
            assert base_at.endswith(CONSONANTS)

        if pronoun in (Pronoun.ANI, Pronoun.ATA, Pronoun.HU, Pronoun.HI, Pronoun.ANACNU):
            return base
        if pronoun == Pronoun.AT:
            return base_at + "i" + ("!" if base.endswith("E!H") else "")
        if pronoun in (Pronoun.ATEM, Pronoun.HEM):
            return base_at + "u" + ("!" if base.endswith("E!H") else "")
        if pronoun in (Pronoun.ATEN, Pronoun.HEN):
            base = base.replace("Á", "")
            if base.endswith("E!H"):
                return base[:-3] + "E!YnaH"
            base = base.replace("i!", "e!")
            if base.endswith("n"):
                return base[:-1] + "_naH"
            if re.search(r"e![jhR]$", base):
                return base.replace("e!", "A!") + "naH"
            if re.search(r"e!Q$", base):
                return base.replace("e!", "E!") + "naH"
            return base.replace("Á", "") + ("3" if base[-3] in "aiueoWY" else "") + "naH"
    elif binyan == Binyan.NIFAL:
        assert base[:2] in ("ye", "yI")

        if pronoun == Pronoun.ANI:
            if re.fullmatch(r"yI_.A!.", base):
                return "Q" + base[1:]
            return "Q" + ("E" if base[1] == "I" else "e") + base[2:]

        base = base[1:]
        base = PRONOUN_FUTURE_PREFIX[pronoun] + base
        base_at = base.replace("Á", "")
        stressed_suffix_at = True
        if base_at.endswith("E!H"):
            base_at = base_at[:-3]
        elif Paradigm.KFULIM == paradigm and not re.search(r"(.).!\1", base_at):
            if base_at[-1] in "r":
                base_at = base_at.replace("A!", "a!")
            else:
                base_at = base_at[:-1] + ("" if base_at[-1] in GRONIYOT else "_") + add_dagesh_lene(base_at[-1])
            stressed_suffix_at = False
        else:
            assert base_at.endswith(CONSONANTS)
            base_at = re.sub(
                ".!", "á" if base_at[-4] in GRONIYOT else "3", base_at)

        if pronoun in (Pronoun.ATA, Pronoun.HU, Pronoun.HI, Pronoun.ANACNU):
            return base
        if pronoun == Pronoun.AT:
            return base_at + "i" + ("!" if stressed_suffix_at else "")
        if pronoun in (Pronoun.ATEM, Pronoun.HEM):
            return base_at + "u" + ("!" if stressed_suffix_at else "")
        if pronoun in (Pronoun.ATEN, Pronoun.HEN):
            if base.endswith("E!H"):
                return base[:-3] + "E!YnaH"
            if base.endswith("n"):
                return base[:-1] + "_naH"
            if re.search(r".!Q$", base):
                return re.sub(".!", "E!", base) + "naH"
            return base.replace("Á", "") + ("3" if base[-3] in "aiueoWY" else "") + "naH"
    elif binyan == Binyan.HUFAL:
        assert base[:2] in ("yU", "yu")
        base = PRONOUN_FUTURE_PREFIX[pronoun] + base[1:]

        base_at = base.replace("Á", "")
        stressed_suffix_at = True
        if base_at.endswith("E!H"):
            base_at = base_at[:-3]
        elif Paradigm.KFULIM == paradigm and len(base_at) == 6 and base_at[-4] == "j":
            base_at = base_at[:-1] + ("" if base_at[-1] in GRONIYOT else "_") + add_dagesh_lene(base_at[-1])
            stressed_suffix_at = False
        else:
            assert base_at.endswith(CONSONANTS)
            base_at = re.sub("[aA]!", "á" if base_at[-4] in GRONIYOT else "3", base_at)

        if pronoun in (Pronoun.ANI, Pronoun.ATA, Pronoun.HU, Pronoun.HI, Pronoun.ANACNU):
            return base
        if pronoun == Pronoun.AT:
            return base_at + "i" + ("!" if stressed_suffix_at else "")
        if pronoun in (Pronoun.ATEM, Pronoun.HEM):
            return base_at + "u" + ("!" if stressed_suffix_at else "")
        if pronoun in (Pronoun.ATEN, Pronoun.HEN):
            if base.endswith("E!H"):
                return base[:-3] + "E!YnaH"
            if base.endswith("n"):
                return base[:-1] + "_naH"
            if re.search(r".!Q$", base):
                return re.sub(".!", "E!", base) + "naH"
            return base.replace("Á", "") + ("3" if base[-3] in "aiueoWY" else "") + "naH"
    elif binyan == Binyan.PAAL:
        base = base[1:]

        if pronoun == Pronoun.ANI:
            if base[:2] == "oQ":
                return "Qo" + base[2:]
            if Paradigm.PE_YOD == paradigm:
                return "Q" + base
            if base[0].islower():
                return "Q" + ("e" if base[0] in "ie" else "a") + base[1:]
            if base[1] in GRONIYOT:
                return "QE" + base[1:].replace("á", "é")
            return "Q" + ("E" if base[0] in "IE" else "A") + base[1:]

        base = PRONOUN_FUTURE_PREFIX[pronoun] + base
        base_at = base.replace("Á", "")
        if base_at.endswith("E!H"):
            base_at = base_at[:-3]
        elif Paradigm.PE_YOD == paradigm:
            base_at = re.sub(".!", "á" if base_at[-4] in GRONIYOT else "3" , base_at)
        elif Paradigm.KFULIM == paradigm and len(base_at) == 6:
            base_at = base_at[:-1] + ("" if base_at[-1] in GRONIYOT else "_") + add_dagesh_lene(base_at[-1])
        else:
            assert base_at.endswith(CONSONANTS)
            if re.fullmatch(r"....!.", base_at):
                pass  # do nothing
            elif "á" in base_at:  # FIXME
                base_at = re.sub(f".!", "", base_at.replace("á", "A"))
            elif "é" in base_at:  # FIXME
                base_at = re.sub(f".!", "", base_at.replace("é", "E"))
            else:
                base_at = re.sub(
                    f".!", "á" if base_at[-4] in GRONIYOT else "3", base_at)

        if pronoun in (Pronoun.ATA, Pronoun.HU, Pronoun.HI, Pronoun.ANACNU):
            return base
        if pronoun == Pronoun.AT:
            return base_at + "i" + ("" if "!" in base_at else "!")
        if pronoun in (Pronoun.ATEM, Pronoun.HEM):
            return base_at + "u" + ("" if "!" in base_at else "!")
        if pronoun in (Pronoun.ATEN, Pronoun.HEN):
            base = base.replace("Á", "")
            if Paradigm.AYIN_WAW == paradigm and base.endswith("j"):
                return re.sub(".!", "A!", base) + "naH"
            if base.endswith("E!H"):
                return base[:-3] + "E!YnaH"
            if re.search(r".!Q$", base):
                return (re.sub(".!", "E!", base) + "naH").replace("nn", "_n")
            if "i!" in base:
                return re.sub("n3?n", "_n", base.replace("i!", "e!") + ("3" if base[-3] in "aiueoWY" else "") + "naH")
            if "u!" in base:
                return re.sub("n3?n", "_n", base.replace("u!", "o!") + ("3" if base[-3] in "aiueoWY" else "") + "naH")
            return re.sub("n3?n", "_n", base + ("3" if base[-3] in "aiueoWY" else "") + "naH")

def inflect_past(base: str, binyan: Binyan, pronoun: Pronoun, paradigm: Paradigm) -> str:
    if pronoun == Pronoun.HU:
        return base
    base = base.replace("Á", "")
    if base.endswith("a!H"):
        if binyan in (Binyan.NIFAL, Binyan.PUAL, Binyan.HITPAEL, Binyan.HUFAL, Binyan.HIFIL):
            base = base.replace("a!H", "e!Y")
        else:
            base = base.replace("a!H", "i!")
    if pronoun in (Pronoun.ANI, Pronoun.ATA, Pronoun.AT, Pronoun.ANACNU):
        if binyan == Binyan.PAAL and Paradigm.KFULIM == paradigm and re.fullmatch(r"..!.", base):
            if base[-1] in GRONIYOT + ("r",):
                return re.sub(".!", "a" if base[-1] not in "j" else "A", base) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
            return base.replace("!", "")[:-1] + "_" + add_dagesh_lene(base[-1]) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        if binyan == Binyan.NIFAL and Paradigm.KFULIM == paradigm and re.fullmatch(r"na.A!.", base):
            return "n3" + base[2] + "A" + add_dagesh_forte(base[-1]) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        if re.search(r"[aiueoAIUEOW]!?Y?$", base):
            res = base + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        elif base.endswith("Q") and len(base) != 3 and binyan != Binyan.PAAL:
            res = re.sub(r"[aieA]!", "e!", base) + \
                PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        elif base.endswith("Q") and binyan == Binyan.PAAL and base[-3] in "ae":
            res = base + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        else:
            res = re.sub(r"[aieA]!", "A!", base) + PRONOUN_PAST_SUFFIX[pronoun]
        res = res.replace("nn", "_n").replace("tT", "_T")
        return res
    if pronoun in (Pronoun.ATEM, Pronoun.ATEN):
        if binyan == Binyan.PAAL and Paradigm.KFULIM == paradigm and re.fullmatch(r"..!.", base):
            if base[-1] in GRONIYOT + ("r",):
                return re.sub(".!", "a" if base[-1] not in "j" else "A", base) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
            return base.replace("!", "")[:-1] + "_" + add_dagesh_lene(base[-1]) + "W" + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        if re.search(r"[aiueoAIUEOW]!?Y?$", base):
            res = base.replace("!", "") + \
                PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        elif base.endswith("Q") and len(base) != 3 and binyan != Binyan.PAAL:
            res = re.sub(r"[aieA]!", "e", base) + \
                PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        elif base.endswith("Q") and binyan == Binyan.PAAL and base[-3] in "ae":
            res = base.replace("!", "") + \
                PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        else:
            res = re.sub(r"[aieA]!", "A", base) + PRONOUN_PAST_SUFFIX[pronoun]
        if binyan == Binyan.PAAL and len(res) > 3 + len(PRONOUN_PAST_SUFFIX[pronoun]):
            res = res[0] + ("á" if res[0] in GRONIYOT else "3") + res[2:]
        elif binyan == Binyan.HIFIL and re.fullmatch(r"he[QRjh][ie]!.", base):
            res = "hA" + base[2] + "A" + base[-1] + PRONOUN_PAST_SUFFIX[pronoun]
        elif binyan == Binyan.HIFIL and re.match(r"he.A..{4}", res):
            res = res[0] + "á" + res[2:]
        res = res.replace("tT", "_T")
        return res
    assert pronoun in (Pronoun.HI, Pronoun.HEM, Pronoun.HEN)
    if re.search(r"[aiueoAIUEOW]!?Y?$", base):
        if pronoun == Pronoun.HI:
            res = re.sub(r"[aiueoAIUEOW]!?Y?$", "", base)
            if re.search(r"é.$", res):
                return re.sub(r"é(?=.$)", "E", res) + "ta!H"
            if re.search(r"á.$", res):
                return re.sub(r"á(?=.$)", "A", res) + "ta!H"
            return res + ("á" if res.endswith(GRONIYOT) else "3") + "ta!H"
        return re.sub(r"[aiueoAIUEOW]!?Y?$", "", base) + PRONOUN_PAST_SUFFIX[pronoun]
    if Paradigm.KFULIM == paradigm and binyan in (Binyan.PAAL, Binyan.NIFAL, Binyan.HIFIL) and not (add_dagesh_lene(base[-1]) == add_dagesh_lene(base[-4]) and re.search(r"..!.$", base)):#not re.search(r"(.).!\1$", re.sub("(.).![fvxdgt]$", lambda m: add_dagesh_lene(m[0]), base)):
        return base[:-1] + ("" if base[-1] in "QRhjr" else "_") + add_dagesh_lene(base[-1]) + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
    if binyan == Binyan.HIFIL:
        return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
    else:
        if binyan == Binyan.PAAL and len(base) == 4:
            return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
        if re.search(r"é..!", base):
            return re.sub(r"(.)\1", r"\1%\1", re.sub(r"é(.).!", r"E\1", base)).replace("%", "3") + PRONOUN_PAST_SUFFIX[pronoun]
        if re.search("á..!", base):
            return re.sub(r"(.)\1", r"\1%\1", re.sub(r"á(.).!", r"A\1", base)).replace("%", "3") + PRONOUN_PAST_SUFFIX[pronoun]
        if binyan == Binyan.NIFAL and re.search("W!.$", base):
            return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
        return re.sub(r"[Aae]!", "á" if base[-4] in GRONIYOT else "3", base) + PRONOUN_PAST_SUFFIX[pronoun]

def inflect_present(base: str, binyan: Binyan, param: Present, paradigm: Paradigm) -> str:
    if param == Present.MALE_SINGULAR:
        return base
    if binyan in (Binyan.HITPAEL, Binyan.PIEL) or binyan == Binyan.PAAL and re.fullmatch(".W.e!.Á?|.[aW].E!H", base):
        if param == Present.FEMALE_SINGULAR:
            if base.endswith("e!Q") and binyan in (Binyan.HITPAEL, Binyan.PIEL):
                return base + "t"
            if re.search("e!.Á?$", base):
                return re.sub(r"e!(.)Á?$", lambda m: ("A!" + m[1] + "At") if m[1] in GRONIYOT else ("E!" + m[1] + "Et"), base)
            if base.endswith("E!H"):
                # alternatively: "a!H" -> "eYt"
                return base.replace("E!H", "a!H")
        if param == Present.MALE_PLURAL:
            if re.search("e!.Á?$", base):
                if re.search(r"á.e!.Á?$", base):
                    return re.sub(r"á(.)e!", r"A\1", base.replace("Á", "")) + "i!m"
                return re.sub(r"(.)e!(.)Á?$", lambda m: m[1] + ("á" if m[1] in GRONIYOT else "3") + m[2], base) + "i!m"
            if base.endswith("E!H"):
                return base.replace("E!H", "i!m")
        if param == Present.FEMALE_PLURAL:
            if re.search("e!.Á?$", base):
                if re.search(r"á.e!.Á?$", base):
                    return re.sub(r"á(.)e!", r"A\1", base.replace("Á", "")) + "W!t"
                return re.sub(r"(.)e!(.)Á?$", lambda m: m[1] + ("á" if m[1] in GRONIYOT else "3") + m[2], base) + "W!t"
            if base.endswith("E!H"):
                return base.replace("E!H", "W!t")
    if binyan in (Binyan.PUAL, Binyan.HUFAL, Binyan.NIFAL):
        if param == Present.FEMALE_SINGULAR:
            if base.endswith("a!Q"):
                return base[:-3] + "e!Qt"
            if re.search("a!.$", base):
                return re.sub(r"a!(.)", lambda m: ("A!" + m[1] + "At") if m[1] in GRONIYOT else ("E!" + m[1] + "Et"), base)
            if base.endswith("E!H"):
                if binyan in (Binyan.NIFAL, Binyan.HUFAL):
                    return base.replace("E!H", "e!Yt")
                # alternatively: "a!H" -> "eYt"
                return base.replace("E!H", "a!H")
        if param == Present.MALE_PLURAL:
            if re.search("a!.$", base):
                return base.replace("a!", "a") + "i!m"
            if base.endswith("E!H"):
                return base.replace("E!H", "i!m")
        if param == Present.FEMALE_PLURAL:
            if re.search("a!.$", base):
                return base.replace("a!", "a") + "W!t"
            if base.endswith("E!H"):
                return base.replace("E!H", "W!t")
    if binyan == Binyan.HIFIL:
        if re.fullmatch("me.e![^Rr]Á?", base):
            return "m3" + base[2] + "I" + add_dagesh_forte(base[5]) + {
                Present.FEMALE_SINGULAR: "a!H",
                Present.MALE_PLURAL: "i!m",
                Present.FEMALE_PLURAL: "W!t"
            }[param]
        if re.match("me[^Y]", base):
            base = "m3" + base[2:]
        if re.search("[" + "".join(CONSONANTS) + "]Á?$", base):
            return base.replace("!", "").replace("Á", "") + {
                Present.FEMALE_SINGULAR: "a!H",
                Present.MALE_PLURAL: "i!m",
                Present.FEMALE_PLURAL: "W!t"
            }[param]
        if base.endswith("E!H"):
            return base[:-3] + {
                Present.FEMALE_SINGULAR: "a!H",
                Present.MALE_PLURAL: "i!m",
                Present.FEMALE_PLURAL: "W!t"
            }[param]
    if binyan == Binyan.PAAL:
        if re.fullmatch(".a!.", base):
            return base.replace("!", "") + PRESENT_SUFFIX[param]
        if re.fullmatch(".A!.", base):
            if base.endswith(GRONIYOT + ("r", )):
                base = base.replace("A!", "a")
            else:
                base = base[:-2] + add_dagesh_forte(base[-1])
            return base + PRESENT_SUFFIX[param]
        if re.fullmatch(".a.e!.Á?", base):
            return base[0] + ("á" if base[0] in GRONIYOT else "3") + base[2:].replace("!", "").replace("Á", "") + PRESENT_SUFFIX[param]

def future2infinitive(base: str, binyan: Binyan, paradigm: Paradigm) -> Optional[str]:
    assert binyan not in (Binyan.PUAL, Binyan.HUFAL)
    if binyan in (Binyan.HIFIL, Binyan.NIFAL, Binyan.HITPAEL):
        return "l3h" + base[1:].replace("E!H", "W!t")
    if binyan == Binyan.PIEL:
        return "l" + base[1:].replace("E!H", "W!t")
    if binyan == Binyan.PAAL:
        if base.endswith("E!H"):
            return "l" + base[1:].replace("E!H", "W!t")
        return "l" + re.sub("[^iu]!(.)Á?$", lambda m: "o!" + m[1] + ("Á" if m[1] in GRONIYOT else ""), base[1:])

def past2future(base: str, binyan: Binyan, paradigm: Paradigm) -> Optional[str]:
    if binyan == Binyan.HITPAEL:
        return "y" + base[1:].replace("a!H", "E!H")
    if binyan in (Binyan.PIEL, Binyan.PUAL):
        base = "y3" + remove_dagesh_lene(base[0]) + re.sub("^[Ie]", "a" if re.search("e[rQ].!", base) else "A", base[1:])
        return base.replace("a!H", "E!H")
    if binyan == Binyan.HIFIL:
        base = base.replace("a!H", "E!H")
        if re.match("^hE.é", base):
            return "y" + "A" + base[2] + "á" + base[4:]
        vowel = "A"
        if base[1:3] == "eY":
            vowel = "e"
        elif base[1] in "aiueo":
            vowel = "a"
        elif base[1] == "W":
            vowel = "W"
        return "y" + vowel + base[2:]
    if binyan == Binyan.HUFAL:
        return "y" + base[1:].replace("a!H", "E!H")
    if binyan == Binyan.NIFAL:
        if (m := re.fullmatch(r"n(?:I_?|W)(.)A!(.)", base)):
            return "yI_" + ("w" if base[1] == "W" else "n") + "a" + remove_dagesh_lene(m[1]) + ("A" if m[2] in "Rjh" else "e") + "!" + m[2]
        if (m := re.fullmatch(r"n(?:I_?|W)(.)a!H", base)):
            return "yI_" + ("w" if base[1] == "W" else "n") + "a" + remove_dagesh_lene(m[1]) + "E!H"
        if (m := re.fullmatch(r"n(?:I_?|W)(.)a!Q", base)):
            return "yI_" + ("w" if base[1] == "W" else "n") + "a" + remove_dagesh_lene(m[1]) + "e!Q"
        if (m := re.fullmatch(r"na(.)A!.", base)):
            return "yI_" + add_dagesh_lene(m[1]) + base[3:]
        if (m := re.fullmatch(r"ne([QRhjr])A!(.)", base)):
            return "ye" + m[1] + "A!" + m[2]
        if (m := re.fullmatch(r"na(.)W!.", base)):
            return "yI_" + add_dagesh_lene(m[1]) + base[3:]
        base = base[2:].replace("!", "")
        # FIXME
        if not base.endswith("aH") and len(base) < 4:
            return None
        if re.match("^.é", base):
            base = re.sub(r"(?<=^.)é", "", base)
        return "y" + ("e" if base[0] in GRONIYOT + ("r", ) else "I_") + add_dagesh_lene(base[0]) + "a" + remove_dagesh_lene(base[1]) + ("E!H" if base.endswith("aH")  else ("A" if base[3] in "hjR" else "e") + "!" + base[3])
    if binyan == Binyan.PAAL:
        if (m := re.fullmatch(r"(.)a(.)A!(.)", base)):
            if Paradigm.PE_ALEF == paradigm:
                return "yoQ" + m[2] + "A!" + m[3]
            if m[1] in "QhRj" and paradigm in (Paradigm.PAAL_3, Paradigm.PAAL_4):
                return "yE" + m[1] + "é" + m[2] + "A!" + m[3]
            if paradigm in (Paradigm.PAAL_1, Paradigm.PAAL_4):
                if m[1] in "QhRj":
                    return "yE" + m[1] + "é" + m[2] + "o!" + m[3]
                if m[1] == "n":
                    return "yI" + (add_dagesh_forte(m[2]) if m[2] not in "QRjhr" else "n" + m[2]) + ("A" if m[2] in "hjR" or m[3] in "QRjh" else "o") + "!" + m[3]
                if m[1] == "y":
                    return "yi" + m[2] + "A!" + m[3]
                if m[2] == m[3]:
                    return "ya" + remove_dagesh_lene(m[1]) + "o!" + m[3]
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            if Paradigm.PAAL_2 == paradigm:
                if m[1] in "RjQh":
                    return "yA" + m[1] + add_dagesh_lene(m[2]) + "o!" + m[3]
                if m[1] == "n":
                    return "yI" + (add_dagesh_forte(m[2]) if m[2] not in "QRjhr" else "n" + m[2]) + "A!" + m[3]
                if m[1] == "y":
                    return "ye" + m[2] + ("A!" if m[3] in "Rjh" else "e!") + m[3]
                # if m[1] in "Qh":
                #     return "yE" + m[1] + add_dagesh_lene(m[2]) + "o!" + m[3]
            if m[1] in "RjQh":
                return "yA" + m[1] + "á" + m[2] + "o!" + m[3]
            if m[2] in "QhjR" or m[3] in "QhjR":
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "o!" + m[3]
        if re.fullmatch(r".a!.", base):
            if Paradigm.PAAL_1 == paradigm:
                return "ya" + remove_dagesh_lene(base[0]) + "i!" + base[-1] + ("Á" if base[-1] in "Rhj" else "")
            return "ya" + remove_dagesh_lene(base[0]) + "u!" + base[-1] + ("Á" if base[-1] in "Rhj" else "")
        if re.fullmatch(r".A!.", base):
            if Paradigm.PAAL_1 == paradigm:
                return "ya" + remove_dagesh_lene(base[0]) + "o!" + base[-1] + ("Á" if base[-1] in "Rhj" else "")
            if Paradigm.PAAL_2 == paradigm:
                return "yI" + add_dagesh_forte(base[0]) + "o!" + base[-1] + ("Á" if base[-1] in "Rhj" else "")
            return "ye" + remove_dagesh_lene(base[0]) + "A!" + base[-1]
        if re.fullmatch(r".a.a!H", base):
            if Paradigm.PAAL_1 == paradigm:
                if base[0] in "QhjR":
                    return "yE" + base[0] + "é" + base[2] + "E!H"
                if base[0] == "n":
                    return "yI" + (add_dagesh_forte(base[2]) if base[2] not in "QRjhr" else "n" + base[2]) + "E!H"
                if base[0] == "y":
                    return "yi" + base[2] + "E!H"
                assert False
            if Paradigm.PAAL_2 == paradigm:
                if base[0] in "RjQh":
                    return "yA" + base[0] + add_dagesh_lene(base[2]) + "E!H"
            if base[0] in "RjQh":
                return "yA" + base[0] + "á" + base[2] + "E!H"
            return "yI" + remove_dagesh_lene(base[0]) + add_dagesh_lene(base[2]) + "E!H"

def past2present(base: str, binyan: Binyan, paradigm: Paradigm) -> Optional[str]:
    if binyan == Binyan.HITPAEL:
        return "m" + base[1:].replace("a!H", "E!H")
    if binyan in (Binyan.PIEL, Binyan.PUAL):
        base = re.sub("A!", "a!", base)
        base = "m3" + remove_dagesh_lene(base[0]) + re.sub("^[Ie]", "a" if re.search("e[rQ].!", base) else "A", base[1:])
        return base.replace("a!H", "E!H")
    if binyan == Binyan.HIFIL:
        base = base.replace("a!H", "E!H")
        if re.match("^hE.é", base):
            return "m" + "A" + base[2] + "á" + base[4:]
        if re.fullmatch("he..!.Á?", base):
            return "m" + base[1:]
        if base[1:3] == "eY" or base[1] in "aW":
            return "m" + base[1:]
        if base[1] in "iueo":
            return "ma" + base[2:]
        return "mA" + base[2:]
    if binyan == Binyan.HUFAL:
        base = re.sub("A!", "a!", base)
        return "m" + base[1:].replace("a!H", "E!H")
    if binyan == Binyan.NIFAL:
        if re.fullmatch(r"n(?:I_?|W)(.)A!(.)", base) or re.fullmatch(r"na(.)A!.", base):
            return base.replace("A!", "a!")
        if re.match(r"n[IE].é?.A!.", base):
            return base.replace("A!", "a!")
        return base.replace("a!H", "E!H")
    if binyan == Binyan.PAAL:
        if re.fullmatch(r".a.A!.", base):
            if paradigm == Paradigm.PAAL_4:
                return base[0] + "a" + base[2] + "e!" + base[-1] + ("Á" if base[-1] in GRONIYOT else "")
            return base[0] + "W" + base[2] + "e!" + base[-1] + ("Á" if base[-1] in GRONIYOT else "")
        if re.fullmatch(r".a.a!H", base):
            if paradigm == Paradigm.PAAL_4:
                return base[0] + "a" + base[2] + "E!H"
            return base[0] + "W" + base[2] + "E!H"
        if re.fullmatch(r".[aA]!.", base):
            return base
        if re.fullmatch(r".a.a!Q", base):
            if paradigm == Paradigm.PAAL_1:
                return base[0] + "W" + base[2] + "e!Q"
            return base[0] + "W" + base[2] + "a!Q"
        if re.fullmatch(r".a.e!Q", base):
            return base
        return base

def past2binyan(verb: str, paradigm: Paradigm) -> Optional[Binyan]:
    if re.fullmatch(".a.(A!.|a!H|a!Q)", verb):
        return Binyan.PAAL
    if re.fullmatch(".[aA]!.", verb):
        return Binyan.PAAL
    if paradigm in {Paradigm.PE_YOD, Paradigm.AYIN_WAW, Paradigm.PAAL_1, Paradigm.PAAL_2}:
        return Binyan.PAAL
    if re.fullmatch("hI..(i!.Á?|a!H)", verb):  # must be before PIEL and HITPAEL
        return Binyan.HIFIL
    if re.fullmatch("h(eY?.|E[rjhQR]é?.|W.)(i!.Á?|a!H)|he.e!.Á?", verb):
        return Binyan.HIFIL
    if re.match("hI(t.|[csS]T|Z7|zD)", verb) or re.fullmatch("hI_[7TD](A(.á?.|[rhjRQ])|a[rQ])(e!.Á?|a!H|a!Q)", verb):
        return Binyan.HITPAEL
    if re.fullmatch("nI..(A!.|a!Q)", verb) or re.fullmatch("n(I.|E[jRhQ]é?).a!H", verb) or re.fullmatch("nE[jRhQ]é?.(A!.|a!Q)", verb) or re.fullmatch("nW.A!.", verb) or re.fullmatch("nI[rjhRQ]A!.", verb):
        return Binyan.NIFAL
    if re.fullmatch(".(I.á?.|I..3.|[Ie][jRQhr])(e!.Á?|a!H)", verb) or re.fullmatch(r".W(.)e!.Á?", verb):
        return Binyan.PIEL
    if re.fullmatch("h(U.|u).(A!.|a!H|a!Q)", verb):  # must be before PUAL
        return Binyan.HUFAL
    if re.fullmatch(".(U.á?.|[Uo][jRQhr])(A!.|a!H|a!Q)", verb) or re.fullmatch(r".W(.)A!\1", verb):
        return Binyan.PUAL
    return None

def __inflect(base: str, binyan: Binyan, paradigm: Paradigm) -> Optional[dict[str, str]]:
    res = {}
    future_base = past2future(base, binyan, paradigm)
    if future_base is None:
        return None
    present_base = past2present(base, binyan, paradigm)
    if present_base is None:
        return None
    for pronoun in Pronoun:
        res["past_" + pronoun.name] = fixup(inflect_past(base, binyan, pronoun, paradigm))
    for pronoun in Pronoun:
        res["future_" + pronoun.name] = fixup(inflect_future(future_base, binyan, pronoun, paradigm))
    for param in Present:
        res["present_" + param.name] = fixup(inflect_present(present_base, binyan, param, paradigm) or "")  # FIXME
    if binyan not in (Binyan.PUAL, Binyan.HUFAL):
        res["shem_poal"] = fixup(future2infinitive(future_base, binyan, paradigm) or "")
    return res

def inflect(verb: str, paradigm: Paradigm) -> Optional[dict[str, str]]:
    binyan = past2binyan(verb, paradigm)
    if binyan is None:
        return None
    return __inflect(verb, binyan, paradigm)
