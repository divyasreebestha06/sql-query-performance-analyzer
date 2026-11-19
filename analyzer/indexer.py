import re
from typing import List

class IndexRecommender:
    @staticmethod
    def recommend(query: str) -> List[str]:
        recommendations = []
        # Find table and where clauses
        table_match = re.search(r"FROM\s+([a-zA-Z0-9_]+)", query, re.IGNORECASE)
        where_match = re.search(r"WHERE\s+(.*?)(?:ORDER|GROUP|LIMIT|$)", query, re.IGNORECASE)

        if table_match and where_match:
            table = table_match.group(1)
            where_clause = where_match.group(1)
            # Find column predicates
            cols = re.findall(r"([a-zA-Z0-9_]+)\s*(=|LIKE|>|<|IN)", where_clause, re.IGNORECASE)
            indexed_cols = [c[0] for c in cols if c[0].lower() not in ("and", "or", "not")]
            if indexed_cols:
                col_list = ", ".join(indexed_cols[:2])
                idx_name = f"idx_{table}_{'_'.join(indexed_cols[:2])}"
                recommendations.append(f"CREATE INDEX {idx_name} ON {table} ({col_list});")

        return recommendations
