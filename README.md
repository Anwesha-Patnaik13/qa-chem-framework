# QA Testing Framework for a Molecular Weight Calculator

An automated test suite for a small scientific program that calculates molecular weights from chemical formulas (for example, H2O gives about 18.015 g/mol). The project demonstrates test design, scientific validation, error handling, regression testing, automated reporting and mutation testing.

## What is tested

| Area | Examples |
|---|---|
| Scientific correctness | H2O (18.015), CO2 (44.009), NaCl, CH4, O2, glucose (C6H12O6) |
| Empty input | Empty string, spaces only and None raise a clear error |
| Invalid formulas | Lowercase (h2o), symbols (H2O!), numbers only (123), unknown element (Xx), zero count (H0) |
| Impossible values | A negative molecular weight is rejected |
| Zero counts inside longer formulas | H0O and C0H4 are rejected |

Decimal results are compared with a tolerance (`pytest.approx`) instead of exact equality, because floating-point numbers are not stored exactly.

## Project structure

```
qa-chem-framework/
├── src/molecular_weight.py          # program under test
├── tests/test_molecular_weight.py   # pytest test suite
├── conftest.py                      # writes CSV/Excel reports after each run
├── pytest.ini                       # pytest settings
└── reports/                         # test_report.csv and test_report.xlsx
```

## How to run

```
conda create -n qa-chem python=3.11 -y
conda activate qa-chem
pip install pytest pytest-cov pandas openpyxl
pytest -v
```

After each run, results are saved to `reports/test_report.csv` and `reports/test_report.xlsx` (a Summary sheet and a Results sheet).

## Test results

All 19 tests pass on the correct code.

## Mutation testing results

I deliberately introduced bugs into the calculator, one at a time, and checked whether the test suite detected them. After each run the original code was restored.

| Bug introduced | Tests failed | Caught? |
|---|---|---|
| Hydrogen weight 1.008 changed to 2.008 | 3 | Yes |
| Oxygen weight 15.999 changed to 16.999 | 4 | Yes |
| Empty input accepted | 2 | Yes |
| Atom counts ignored (H2O treated as HO) | 6 | Yes |
| Negative weight accepted | 1 | Yes |
| Zero counts accepted (H0) | 0 | No (test gap found) |
| Zero counts accepted, after adding H0O and C0H4 tests | 2 | Yes |

The zero-count bug was not caught by the original tests. The `H0` test still passed because a second check (total weight must be positive) rejected it anyway. A formula like `H0O` would slip through, because the total weight stays positive. This is a gap in test coverage found through mutation testing. Adding tests for `H0O` and `C0H4` closed the gap.