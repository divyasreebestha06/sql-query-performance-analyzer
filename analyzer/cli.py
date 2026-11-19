import json
import sys
from analyzer.engine import QueryAnalyzer
from analyzer.indexer import IndexRecommender

def main():
    analyzer = QueryAnalyzer()
    query = sys.argv[1] if len(sys.argv) > 1 else "SELECT * FROM users WHERE email = 'test@example.com'"
    report = analyzer.analyze(query)
    report["index_suggestions"] = IndexRecommender.recommend(query)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
