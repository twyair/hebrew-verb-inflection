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


class Gizra(Enum):
    KFULIM = auto()
    PY = auto()
    AYIN_WAW = auto()

    def from_root(root: str) -> set[Gizra]:
        res = set()
        if root.startswith("y"):
            res.add(Gizra.PY)
        if len(root) == 3 and root[1] == root[2]:
            res.add(Gizra.KFULIM)
        if len(root) == 3 and root[1] == "w":
            res.add(Gizra.AYIN_WAW)
        return res


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
ALTERNATIVE_PAAL = {'barA!x', 'nadA!j', 'qarA!n', 'laRA!7', 'cajA!d', 'ZadA!q', 'lahA!g', 'SajA!q', 'nacA!q', 'SagA!v', 'pacA!r', 'baZA!q', 'barA!d', 'caxA!n', '7ajA!n', 'pajA!t', 'cajA!r', 'majA!Z', 'qadA!c', 'nasA!R', 'majA!l', 'mahA!r', 'TacA!c', 'nazA!l', 'DajA!f', 'najA!t', 'GalA!d', 'pajA!r', '7ahA!r', 'DaRA!x', 'naRA!m', 'caQA!r', 'zaRA!q', 'naQA!m', 'caRA!7', 'kavA!d', 'mahA!l', 'lajA!c', 'ZaRA!q', 'rajA!v', 'GaRA!r', 'GaQA!l', 'qadA!m', 'rajA!f', 'naRA!l', 'bajA!r', 'lahA!v', 'nahA!m', 'DavA!q', 'sajA!v', 'laRA!z', 'GavA!r', 'majA!7', '7aRA!n', 'kaQA!v', 'TaQA!r', 'zaRA!f', 'qadA!r', 'basA!m', 'DalA!q', 'ZahA!r', 'baSA!m', 'raxA!v', '7aRA!m', 'ZajA!q', 'ravA!Z', 'baRA!7', 'maRA!l', 'samA!r', 'matA!q', 'TajA!m', 'rajA!Z', 'TahA!d', 'kajA!l', 'maRA!x', 'bajA!c', 'lajA!Z', 'ZamA!q', 'TajA!v', 'GajA!n', 'ZaRA!n', 'ragA!l', 'zahA!r', 'nagA!h', 'lajA!x', 'bagA!r', 'rajA!q', 'caQA!v', 'lajA!m', 'baQA!c', 'raRA!c', 'camA!n', 'cajA!7', 'DacA!n', 'caQA!n', 'ZaRA!r', 'caxA!r', 'najA!l', 'lavA!c', 'paZA!r', 'nahA!g', 'lahA!7', 'samA!q', 'saRA!d', 'cajA!q', 'raQA!m', 'kawA!Z', 'caQA!f', 'natA!r', 'ZalA!l', 'qaZA!r', 'ZaRA!f', 'DaQA!g', 'pahA!q', 'raRA!f', 'laRA!g', 'GaRA!l', 'maRA!d', 'calA!w', 'DajA!s', 'zajA!l', 'baRA!r', 'kaRA!s', 'cajA!f', 'naQA!Z', 'nasA!q', 'zaRA!m', 'qamA!l', 'paRA!r', 'bajA!l', 'kajA!c', 'sajA!7', 'paRA!m', 'ba7A!l', 'ragA!z', 'caQA!7', 'raqA!v', 'DaQA!v', 'naRA!r', 'rahA!7', 'bahA!r', 'ZahA!v', 'caxA!v', 'GajA!x', 'DahA!r', 'raRA!m', 'majA!q', 'laRA!s', 'GaRA!c', 'nasA!j', 'cafA!r', 'naQA!q', 'maRA!7', 'nahA!q', 'ratA!t', 'kacA!l', 'sajA!r', 'saxA!l', 'zahA!v', 'na7A!R', 'caxA!x', 'caQA!g', 'qa7A!n', 'DajA!q', 'paRA!l', 'qarA!v', 'sajA!f', 'rajA!m', 'najA!r', 'calA!m', 'cafA!l', 'pajA!s', 'rahA!v', 'TaQA!v', 'qarA!m', 'nacA!l', 'caQA!l', 'raRA!d', 'zaqA!n', 'baRA!l', 'naRA!Z', 'SaRA!r', 'nagA!R', 'raRA!Z', 'GahA!q', 'GahA!r', 'bacA!l', 'lamA!d', 'bajA!n', 'ragA!c', 'maQA!s', 'qacA!v', 'nafA!j', 'saQA!n', 'bahA!q', 'GadA!l', 'saRA!r', 'ra7A!v', 'qarA!c', 'TaxA!l', 'namA!x', 'rafA!d', 'naQA!f', 'pajA!d', 'laqA!j', 'TaQA!w', 'kacA!r', 'ZahA!l', 'ZaRA!d', 'rajA!c', 'caRA!r', 'raRA!v', 'TaQA!m'}
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

def inflect_future(base: str, binyan: Binyan, pronoun: Pronoun, gizra: set[Gizra]) -> str:
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
        elif Gizra.KFULIM in gizra and base_at[-1] not in "jhQRr" and not re.search(r"(.).!\1$", re.sub("[fvxdgt]$", lambda m: add_dagesh_lene(m[0]), base_at)):
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
        elif Gizra.KFULIM in gizra and not re.search(r"(.).!\1", base_at):
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
        elif Gizra.KFULIM in gizra and len(base_at) == 6 and base_at[-4] == "j":
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
            if Gizra.PY in gizra:
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
        elif Gizra.PY in gizra:
            base_at = re.sub(".!", "á" if base_at[-4] in GRONIYOT else "3" , base_at)
        elif Gizra.KFULIM in gizra and len(base_at) == 6:
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
            if Gizra.AYIN_WAW in gizra and base.endswith("j"):
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

def inflect_past(base: str, binyan: Binyan, pronoun: Pronoun, gizra: set[Gizra]) -> str:
    if pronoun == Pronoun.HU:
        return base
    base = base.replace("Á", "")
    if base.endswith("a!H"):
        if binyan in (Binyan.NIFAL, Binyan.PUAL, Binyan.HITPAEL, Binyan.HUFAL, Binyan.HIFIL):
            base = base.replace("a!H", "e!Y")
        else:
            base = base.replace("a!H", "i!")
    if pronoun in (Pronoun.ANI, Pronoun.ATA, Pronoun.AT, Pronoun.ANACNU):
        if binyan == Binyan.PAAL and Gizra.KFULIM in gizra and re.fullmatch(r"..!.", base):
            if base[-1] in GRONIYOT + ("r",):
                return re.sub(".!", "a" if base[-1] not in "j" else "A", base) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
            return base.replace("!", "")[:-1] + "_" + add_dagesh_lene(base[-1]) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
        if binyan == Binyan.NIFAL and Gizra.KFULIM in gizra and re.fullmatch(r"na.A!.", base):
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
        if binyan == Binyan.PAAL and Gizra.KFULIM in gizra and re.fullmatch(r"..!.", base):
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
    if Gizra.KFULIM in gizra and binyan in (Binyan.PAAL, Binyan.NIFAL, Binyan.HIFIL) and not (add_dagesh_lene(base[-1]) == add_dagesh_lene(base[-4]) and re.search(r"..!.$", base)):#not re.search(r"(.).!\1$", re.sub("(.).![fvxdgt]$", lambda m: add_dagesh_lene(m[0]), base)):
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

def past2future(base: str, binyan: Binyan) -> Optional[str]:
    if binyan == Binyan.HITPAEL:
        return "y" + base[1:]
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
            if base in ALTERNATIVE_PAAL:
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            if m[1] in "Rj":
                return "yA" + m[1] + "á" + m[2] + "o!" + m[3]
            if m[3] in "hjR":
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "o!" + m[3]
        if re.fullmatch(r".a!.", base):
            return "ya" + remove_dagesh_lene(base[0]) + "u!" + base[-1]
        if re.fullmatch(r".a.a!H", base):
            return "yI" + remove_dagesh_lene(base[0]) + add_dagesh_lene(base[2]) + "E!H"

def inflect(base: str, binyan: Binyan, root: str) -> dict[str, str]:
    res = {}
    gizra = Gizra.from_root(root)
    for pronoun in Pronoun:
        res["past_" + pronoun.name] = fixup(inflect_past(base, binyan, pronoun, gizra))
    future_base = past2future(base, binyan)
    if future_base is None:
        return res
    for pronoun in Pronoun:
        res["future_" + pronoun.name] = fixup(inflect_future(future_base, binyan, pronoun, gizra))
    return res
