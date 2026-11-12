"""Molecular weight calculator.

Takes a chemical formula like 'H2O' and returns its molecular weight.
"""

import re

# Atomic weights in g/mol
ATOMIC_WEIGHTS = {
    "H": 1.008,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Na": 22.990,
    "Cl": 35.45,
    "S": 32.06,
    "P": 30.974,
}


def parse_formula(formula):
    """Turn 'H2O' into {'H': 2, 'O': 1}."""
    if not isinstance(formula, str) or formula.strip() == "":
        raise ValueError("Formula cannot be empty")

    formula = formula.strip()

    # Valid formula = only element symbols (capital + optional lowercase) with optional numbers
    if not re.fullmatch(r"([A-Z][a-z]?\d*)+", formula):
        raise ValueError(f"Invalid formula: {formula}")

    counts = {}
    for element, number in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if element not in ATOMIC_WEIGHTS:
            raise ValueError(f"Unknown element: {element}")
        count = int(number) if number else 1
        if count <= 0:
            raise ValueError(f"Invalid count for {element}")
        counts[element] = counts.get(element, 0) + count
    return counts


def molecular_weight(formula):
    """Return the molecular weight of a formula in g/mol."""
    counts = parse_formula(formula)
    weight = sum(ATOMIC_WEIGHTS[el] * n for el, n in counts.items())
    if weight <= 0:
        raise ValueError("Molecular weight must be positive")
    return round(weight, 3)
    