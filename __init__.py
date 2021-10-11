from __future__ import annotations
import re
from typing import Optional

from consts import Binyan, Present, Pronoun
from paradigm import Paradigm

CONSONANTS = tuple("QbvgGdDhwzj7ykxlmnsRpfZqrcStT")
GRONIYOT = tuple("hjQR")
GRONIYOT_RESH = GRONIYOT + ("r", )
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
    if c in GRONIYOT_RESH:
        return c
    else:
        return "_" + add_dagesh_lene(c)

def add_schwa(c: str, hataf: str = "á") -> str:
    assert len(c) == 1
    if c in GRONIYOT:
        return c + hataf
    return c + "3"

def patah_gnuva(c: str) -> str:
    return "Á" if c in "Rhj" else ""

def fixup(word: str) -> str:
    return re.sub(r"(.)\1", lambda m: m[1] + "3" + m[1], word)

def inflect_future(base: str, binyan: Binyan, pronoun: Pronoun, paradigm: Paradigm) -> str:
    if pronoun == Pronoun.HU:
        return base
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
                base_at = base_at[:-4] + add_schwa(base_at[-4]) + base_at[-1]

        if pronoun == Pronoun.ANI:
            return "Q" + ("E" if base.startswith("I") else "á") + base[1:]
        if pronoun in (Pronoun.ATA, Pronoun.HI):
            return "T" + base
        if pronoun == Pronoun.AT:
            return "T" + base_at + "i!"
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
                base_at = base_at[:-1] + add_dagesh_forte(base_at[-1])
            stressed_suffix_at = False
        else:
            assert base_at.endswith(CONSONANTS)
            base_at = re.sub("..!", add_schwa(base_at[-4]), base_at)

        if pronoun in (Pronoun.ATA, Pronoun.HI, Pronoun.ANACNU):
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
            base_at = base_at[:-1] + add_dagesh_forte(base_at[-1])
            stressed_suffix_at = False
        else:
            assert base_at.endswith(CONSONANTS)
            base_at = re.sub(".[aA]!", add_schwa(base_at[-4]), base_at)

        if pronoun in (Pronoun.ANI, Pronoun.ATA, Pronoun.HI, Pronoun.ANACNU):
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
            base_at = re.sub("..!", add_schwa(base_at[-4]) , base_at)
        elif Paradigm.KFULIM == paradigm and len(base_at) == 6:
            base_at = base_at[:-1] + add_dagesh_forte(base_at[-1])
        else:
            assert base_at.endswith(CONSONANTS)
            if re.fullmatch(r"....!.", base_at):
                pass  # do nothing
            elif "á" in base_at:  # FIXME
                base_at = re.sub(f".!", "", base_at.replace("á", "A"))
            elif "é" in base_at:  # FIXME
                base_at = re.sub(f".!", "", base_at.replace("é", "E"))
            else:
                base_at = re.sub(f"..!", add_schwa(base_at[-4]), base_at)

        if pronoun in (Pronoun.ATA, Pronoun.HI, Pronoun.ANACNU):
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
            if base[-1] in GRONIYOT_RESH:
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
            if base[-1] in GRONIYOT_RESH:
                return re.sub(".!", "a" if base[-1] not in "j" else "A", base) + "W" + ("!" if "!" not in PRONOUN_PAST_SUFFIX[pronoun] else "") + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
            return base.replace("!", "")[:-1] + add_dagesh_forte(base[-1]) + "W" + PRONOUN_PAST_SUFFIX[pronoun].replace("T", "t")
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
            res = add_schwa(res[0]) + res[2:]
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
            return res[:-1] + add_schwa(res[-1]) + "ta!H"
        return re.sub(r"[aiueoAIUEOW]!?Y?$", "", base) + PRONOUN_PAST_SUFFIX[pronoun]
    if Paradigm.KFULIM == paradigm and binyan in (Binyan.PAAL, Binyan.NIFAL, Binyan.HIFIL) and not (add_dagesh_lene(base[-1]) == add_dagesh_lene(base[-4]) and re.search(r"..!.$", base)):#not re.search(r"(.).!\1$", re.sub("(.).![fvxdgt]$", lambda m: add_dagesh_lene(m[0]), base)):
        return base[:-1] + add_dagesh_forte(base[-1]) + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
    if binyan == Binyan.HIFIL:
        return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
    else:
        if binyan == Binyan.PAAL and len(base) == 4:
            return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
        if re.search(r"é..!", base):
            return re.sub(r"é(.).!", r"E\1", base) + PRONOUN_PAST_SUFFIX[pronoun]
        if re.search("á..!", base):
            return re.sub(r"á(.).!", r"A\1", base) + PRONOUN_PAST_SUFFIX[pronoun]
        if binyan == Binyan.NIFAL and re.search("W!.$", base):
            return base + PRONOUN_PAST_SUFFIX[pronoun].replace("!", "")
        return re.sub(r".[Aae]!", add_schwa(base[-4]), base) + PRONOUN_PAST_SUFFIX[pronoun]

def inflect_present(base: str, binyan: Binyan, param: Present, paradigm: Paradigm) -> str:
    if param == Present.MALE_SINGULAR:
        return base
    if binyan in (Binyan.HITPAEL, Binyan.PIEL) or binyan == Binyan.PAAL and re.fullmatch(".W.e!.Á?|.[aW].E!H", base):
        if base.endswith("E!H"):
            return base.replace("E!H", PRESENT_SUFFIX[param])
        if param == Present.FEMALE_SINGULAR:
            if base.endswith("e!Q") and binyan in (Binyan.HITPAEL, Binyan.PIEL):
                return base + "t"
            if re.search("e!.Á?$", base):
                return re.sub(r"e!(.)Á?$", lambda m: ("A!" + m[1] + "At") if m[1] in GRONIYOT else ("E!" + m[1] + "Et"), base)
        if param in (Present.MALE_PLURAL, Present.FEMALE_PLURAL):
            if re.search("e!.Á?$", base):
                if re.search(r"á.e!.Á?$", base):
                    return re.sub(r"á(.)e!", r"A\1", base.replace("Á", "")) + PRESENT_SUFFIX[param]
                return re.sub(r"(.)e!(.)Á?$", lambda m: add_schwa(m[1]) + m[2], base) + PRESENT_SUFFIX[param]
    if binyan in (Binyan.PUAL, Binyan.HUFAL, Binyan.NIFAL):
        if base.endswith("E!H"):
            if binyan in (Binyan.NIFAL, Binyan.HUFAL) and param == Present.FEMALE_SINGULAR:
                return base.replace("E!H", "e!Yt")
            return base.replace("E!H", PRESENT_SUFFIX[param])
        if param == Present.FEMALE_SINGULAR:
            if base.endswith("a!Q"):
                return base[:-3] + "e!Qt"
            if re.search("a!.$", base):
                return re.sub(r"a!(.)", lambda m: ("A!" + m[1] + "At") if m[1] in GRONIYOT else ("E!" + m[1] + "Et"), base)
        if param in (Present.MALE_PLURAL, Present.FEMALE_PLURAL):
            if re.search("a!.$", base):
                return base.replace("a!", "a") + PRESENT_SUFFIX[param]
    if binyan == Binyan.HIFIL:
        if re.fullmatch("me.e![^Rr]Á?", base):
            return "m3" + base[2] + "I" + add_dagesh_forte(base[5]) + PRESENT_SUFFIX[param]
        if re.match("me[^Y]", base):
            base = "m3" + base[2:]
        if re.search("[" + "".join(CONSONANTS) + "]Á?$", base):
            return base.replace("!", "").replace("Á", "") + PRESENT_SUFFIX[param]
        if base.endswith("E!H"):
            return base[:-3] + PRESENT_SUFFIX[param]
    if binyan == Binyan.PAAL:
        if re.fullmatch(".a!.", base):
            return base.replace("!", "") + PRESENT_SUFFIX[param]
        if re.fullmatch(".A!.", base):
            if base.endswith(GRONIYOT_RESH):
                base = base.replace("A!", "a")
            else:
                base = base[:-2] + add_dagesh_forte(base[-1])
            return base + PRESENT_SUFFIX[param]
        if re.fullmatch(".a.e!.Á?", base):
            return add_schwa(base[0]) + base[2:].replace("!", "").replace("Á", "") + PRESENT_SUFFIX[param]

def future2infinitive(base: str, binyan: Binyan, paradigm: Paradigm) -> Optional[str]:
    assert binyan not in (Binyan.PUAL, Binyan.HUFAL)
    if binyan in (Binyan.HIFIL, Binyan.NIFAL, Binyan.HITPAEL):
        return "l3h" + base[1:].replace("E!H", "W!t")
    if binyan == Binyan.PIEL:
        return "l" + base[1:].replace("E!H", "W!t")
    if binyan == Binyan.PAAL:
        if base.endswith("E!H"):
            return "l" + base[1:].replace("E!H", "W!t")
        return "l" + re.sub("[^iu]!(.)Á?$", lambda m: "o!" + m[1] + patah_gnuva(m[1]), base[1:])

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
        return "y" + ("e" if base[0] in GRONIYOT_RESH else "I_") + add_dagesh_lene(base[0]) + "a" + remove_dagesh_lene(base[1]) + ("E!H" if base.endswith("aH")  else ("A" if base[3] in "hjR" else "e") + "!" + base[3])
    if binyan == Binyan.PAAL:
        if (m := re.fullmatch(r"(.)a(.)A!(.)", base)):
            if Paradigm.PE_ALEF == paradigm:
                return "yoQ" + m[2] + "A!" + m[3]
            if m[1] in GRONIYOT and paradigm in (Paradigm.PAAL_3, Paradigm.PAAL_4):
                return "yE" + m[1] + "é" + m[2] + "A!" + m[3]
            if paradigm in (Paradigm.PAAL_1, Paradigm.PAAL_4):
                if m[1] in GRONIYOT:
                    return "yE" + m[1] + "é" + m[2] + "o!" + m[3]
                if m[1] == "n":
                    return "yI" + (add_dagesh_forte(m[2]) if m[2] not in GRONIYOT_RESH else "n" + m[2]) + ("A" if m[2] in "hjR" or m[3] in "QRjh" else "o") + "!" + m[3]
                if m[1] == "y":
                    return "yi" + m[2] + "A!" + m[3]
                if m[2] == m[3]:
                    return "ya" + remove_dagesh_lene(m[1]) + "o!" + m[3]
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            if Paradigm.PAAL_2 == paradigm:
                if m[1] in GRONIYOT:
                    return "yA" + m[1] + add_dagesh_lene(m[2]) + "o!" + m[3]
                if m[1] == "n":
                    return "yI" + (add_dagesh_forte(m[2]) if m[2] not in GRONIYOT_RESH else "n" + m[2]) + "A!" + m[3]
                if m[1] == "y":
                    return "ye" + m[2] + ("A!" if m[3] in "Rjh" else "e!") + m[3]
                # if m[1] in "Qh":
                #     return "yE" + m[1] + add_dagesh_lene(m[2]) + "o!" + m[3]
            if m[1] in GRONIYOT:
                return "yA" + m[1] + "á" + m[2] + "o!" + m[3]
            if m[2] in GRONIYOT or m[3] in GRONIYOT:
                return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "A!" + m[3]
            return "yI" + remove_dagesh_lene(m[1]) + add_dagesh_lene(m[2]) + "o!" + m[3]
        if re.fullmatch(r".a!.", base):
            if Paradigm.PAAL_1 == paradigm:
                return "ya" + remove_dagesh_lene(base[0]) + "i!" + base[-1] + patah_gnuva(base[-1])
            return "ya" + remove_dagesh_lene(base[0]) + "u!" + base[-1] + patah_gnuva(base[-1])
        if re.fullmatch(r".A!.", base):
            if Paradigm.PAAL_1 == paradigm:
                return "ya" + remove_dagesh_lene(base[0]) + "o!" + base[-1] + patah_gnuva(base[-1])
            if Paradigm.PAAL_2 == paradigm:
                return "yI" + add_dagesh_forte(base[0]) + "o!" + base[-1] + patah_gnuva(base[-1])
            return "ye" + remove_dagesh_lene(base[0]) + "A!" + base[-1]
        if re.fullmatch(r".a.a!H", base):
            if Paradigm.PAAL_1 == paradigm:
                if base[0] in GRONIYOT:
                    return "yE" + base[0] + "é" + base[2] + "E!H"
                if base[0] == "n":
                    return "yI" + (add_dagesh_forte(base[2]) if base[2] not in GRONIYOT_RESH else "n" + base[2]) + "E!H"
                if base[0] == "y":
                    return "yi" + base[2] + "E!H"
                assert False
            if Paradigm.PAAL_2 == paradigm:
                if base[0] in GRONIYOT:
                    return "yA" + base[0] + add_dagesh_lene(base[2]) + "E!H"
            if base[0] in GRONIYOT:
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
                return base[0] + "a" + base[2] + "e!" + base[-1] + patah_gnuva(base[-1])
            return base[0] + "W" + base[2] + "e!" + base[-1] + patah_gnuva(base[-1])
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
    if paradigm in {Paradigm.PE_YOD, Paradigm.AYIN_WAW, Paradigm.PAAL_1, Paradigm.PAAL_2, Paradigm.PAAL_3, Paradigm.PAAL_4}:
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
