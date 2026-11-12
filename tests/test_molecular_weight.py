import pytest
from src.molecular_weight import molecular_weight, ATOMIC_WEIGHTS


# ---- Correct answers (scientific validation) ----
@pytest.mark.parametrize("formula, expected", [
    ("H2O", 18.015),
    ("CO2", 44.009),
    ("NaCl", 58.44),
    ("CH4", 16.043),
    ("O2", 31.998),
    ("C6H12O6", 180.156),   # glucose
])
def test_known_molecular_weights(formula, expected):
    assert molecular_weight(formula) == pytest.approx(expected, abs=0.01)


# ---- Empty input ----
@pytest.mark.parametrize("bad_input", ["", "   ", None])
def test_empty_input_raises_error(bad_input):
    with pytest.raises(ValueError, match="empty"):
        molecular_weight(bad_input)


# ---- Invalid formulas ----
@pytest.mark.parametrize("bad_formula", ["h2o", "H2O!", "123", "H-2", "Xx", "H0"])
def test_invalid_formula_raises_error(bad_formula):
    with pytest.raises(ValueError):
        molecular_weight(bad_formula)


# ---- Negative molecular weight must be rejected ----
def test_negative_weight_is_rejected(monkeypatch):
    monkeypatch.setitem(ATOMIC_WEIGHTS, "H", -1.0)
    with pytest.raises(ValueError):
        molecular_weight("H")


# ---- Result is always positive ----
def test_weight_is_positive():
    assert molecular_weight("H2O") > 0