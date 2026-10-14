# Lab 5: Static Code Analysis

## Issue Documentation

| No. | Tool | Issue identified | Category | Fix implemented |
|---:|---|---|---|---|
| 1 | Bandit (B608) | SQL query used string interpolation, creating a potential SQL injection vulnerability. | Security | Replaced interpolation with a parameterized SQL query using `?` placeholders. |
| 2 | Pylint (W0102) | `add_stock()` used a mutable list as a default argument. | Correctness | Changed the default to `None` and initialized the list inside the function. |
| 3 | Pylint / Flake8 | Bare `except` clauses could hide unexpected errors. | Reliability | Replaced broad exception handling with specific exception types. |
| 4 | Pylint | Files were opened without context managers and explicit encoding. | Resource management | Used `with open(...)` and UTF-8 encoding. |
| 5 | Pylint | Module and function docstrings were missing. | Maintainability | Added descriptive docstrings. |
| 6 | Flake8 | Unused imports, missing blank lines, and overlong lines were reported. | Style | Removed unused imports and corrected spacing and line lengths. |
| 7 | Pylint | `printStock()` did not follow the standard snake_case naming convention. | Readability | Renamed it to `print_stock()`. |
| 8 | Application logic | Expired medicines could be dispensed. | Correctness and safety | Added an expiry-date check before deducting stock. |

## Verification Results

- Pylint improved from 6.90/10 to 10.00/10.
- Bandit initially identified a possible SQL injection issue and a try/except/pass pattern. The final scan reported no issues.
- Flake8 initially reported style violations. The final scan reported no violations.
- Python compilation completed successfully.
- Runtime checks confirmed that allergy conflicts, unknown patients, and expired medicines are rejected.

## Conclusion

Using Pylint, Bandit, and Flake8 helped identify and address code quality, security, and formatting issues. The updated program is easier to read and maintain, uses safer SQL queries, handles exceptions more carefully, and prevents dispensing expired medicines.
