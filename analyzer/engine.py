from typing import Dict, List, Any
import re

class QueryAnalyzer:
    def __init__(self):
        self.rules = [
            self._check_select_star,
            self._check_leading_wildcard,
            self._check_unindexed_join,
            self._check_missing_limit
        ]

    def _check_select_star(self, query: str) -> Dict[str, Any]:
        if re.search(r"\bSELECT\s+\*", query, re.IGNORECASE):
            return {
                "rule": "AVOID_SELECT_ALL",
                "severity": "WARNING",
                "message": "Using SELECT * retrieves unnecessary columns and bypasses covering indexes."
            }
        return None

    def _check_leading_wildcard(self, query: str) -> Dict[str, Any]:
        if re.search(r"LIKE\s+'%[a-zA-Z0-9]", query, re.IGNORECASE):
            return {
                "rule": "LEADING_WILDCARD_LIKE",
                "severity": "CRITICAL",
                "message": "LIKE '%...' prevents B-tree index usage, causing full table scans."
            }
        return None

    def _check_unindexed_join(self, query: str) -> Dict[str, Any]:
        if re.search(r"\bJOIN\b", query, re.IGNORECASE) and not re.search(r"\bON\b", query, re.IGNORECASE):
            return {
                "rule": "CARTESIAN_PRODUCT",
                "severity": "CRITICAL",
                "message": "JOIN without ON clause creates Cartesian product (O(N*M) complexity)."
            }
        return None

    def _check_missing_limit(self, query: str) -> Dict[str, Any]:
        if re.search(r"\bSELECT\b", query, re.IGNORECASE) and not re.search(r"\bLIMIT\b", query, re.IGNORECASE):
            return {
                "rule": "UNBOUNDED_QUERY",
                "severity": "INFO",
                "message": "Query has no LIMIT clause, risking large memory allocations."
            }
        return None

    def analyze(self, query: str) -> Dict[str, Any]:
        query_clean = " ".join(query.strip().split())
        warnings = []
        for rule in self.rules:
            result = rule(query_clean)
            if result:
                warnings.append(result)

        # Estimate execution score: start at 100
        score = 100
        for w in warnings:
            if w["severity"] == "CRITICAL":
                score -= 35
            elif w["severity"] == "WARNING":
                score -= 15
            elif w["severity"] == "INFO":
                score -= 5

        return {
            "query": query_clean,
            "performance_score": max(0, score),
            "issues": warnings,
            "recommendations_count": len(warnings)
        }
