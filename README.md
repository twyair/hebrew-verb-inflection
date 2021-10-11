# Usage

to conjugate a verb use `inflect()` it takes the verb's base form (past+male+3rd-person+singular/עבר-נסתר) and its conjugation class (one of `Paradigm`'s variants)

to conjugate "שׁ ָמ ַר":

```python
inflect("camA!r", Paradigm.NONE)
```

to conjugate "נ ָפ ַל":

```python
inflect("nafA!l", Paradigm.PAAL_1)
```

`data/bases-minimal.json` contains a set of base forms and their conjugation classes

# TODO

- [X] `inflect_present()`
- [X] `past2present()`
- [X] `past2binyan()`
- [X] `future2infinitive()`