# Usage

to conjugate a verb use `inflect_minimal` it takes the verb's base form (past+male+3rd-person+singular/עבר-נסתר) and its conjugation class (one of `Gizra`'s variants)

to conjugate "שׁ ָמ ַר":

```python
inflect_minimal("camA!r", Gizra.NONE)
```

to conjugate "נ ָפ ַל":

```python
inflect_minimal("nafA!l", Gizra.PAAL_PARADIGM_1)
```

`data/bases-minimal.json` contains a set of base forms and their conjugation classes

# TODO

- [ ] `inflect_present()`
- [ ] `past2present()`
- [X] `past2binyan()`