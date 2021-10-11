from __future__ import annotations
from enum import Enum, auto

from consts import Binyan

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
