# ⚡ sql-query-performance-analyzer

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](analyzer/)
[![SQL](https://img.shields.io/badge/SQL-Analyzer-CC292B?style=for-the-badge&logo=sqlite)](analyzer/)
[![CI](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](ci/)

Database Query Optimizer & EXPLAIN Plan Parser with automatic index recommendation and anti-pattern detection.

## Features
- **Anti-Pattern Detection:** Detects `SELECT *`, leading wildcard `LIKE '%...'`, Cartesian joins, and missing pagination limits.
- **Performance Scoring (0-100):** Weighted risk deduction based on algorithmic complexity and table-scan likelihood.
- **Automated Index Recommendations:** Synthesizes `CREATE INDEX` statements targeting predicate columns in `WHERE` clauses.

## Usage
```bash
python -m analyzer.cli "SELECT * FROM orders WHERE customer_id = 42"
```
