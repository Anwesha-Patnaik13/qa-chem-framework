# QA Testing Framework for a Molecular Weight Calculator

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

The zero-count bug was not caught by the original tests. The `H0` test still passed because a second check (total weight must be positive) rejected it anyway. A formula like `H0O` would slip through, because the total weight stays positive. This is a gap in test coverage found through mutation testing.