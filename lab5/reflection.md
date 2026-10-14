# Lab 5: Reflection on Static Code Analysis

## 1. What did you learn from static code analysis?

I learned that static analysis examines source code without executing it to identify potential bugs, security vulnerabilities, and style violations. Pylint focuses on code quality and maintainability, Bandit checks for common security risks, and Flake8 checks Python style and formatting.

## 2. Which issue was most important, and why?

The potential SQL injection issue was especially important because building SQL queries through string interpolation can allow user input to change the intended query. Parameterized queries separate the SQL statement from the supplied values and reduce this risk.

## 3. How did fixing the issues improve the program?

The fixes improved readability, resource management, exception handling, and input validation. The program now uses parameterized SQL, avoids mutable default arguments, handles expected errors more specifically, and checks allergies, stock availability, and medicine expiry before dispensing.

## 4. What are the limitations of static analysis?

Static analysis cannot guarantee that a program is completely correct or secure. A tool may report false positives, and some runtime or business-logic problems may not be detected. Static analysis should therefore be combined with runtime testing and code review.

## 5. How will you use static analysis in future projects?

I will run static analysis tools regularly during development, prioritize security and correctness issues, review the reports, and rerun the tools after fixing problems. I will also use automated checks before committing or submitting code.
