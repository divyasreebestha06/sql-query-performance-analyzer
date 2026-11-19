import unittest
from analyzer.engine import QueryAnalyzer
from analyzer.indexer import IndexRecommender

class TestQueryAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = QueryAnalyzer()

    def test_clean_query_score(self):
        res = self.analyzer.analyze("SELECT id, username FROM users WHERE status = 'ACTIVE' LIMIT 10")
        self.assertEqual(res["performance_score"], 100)
        self.assertEqual(len(res["issues"]), 0)

    def test_select_star_detection(self):
        res = self.analyzer.analyze("SELECT * FROM orders LIMIT 100")
        rules = [i["rule"] for i in res["issues"]]
        self.assertIn("AVOID_SELECT_ALL", rules)
        self.assertEqual(res["performance_score"], 85)

    def test_leading_wildcard_detection(self):
        res = self.analyzer.analyze("SELECT id FROM users WHERE name LIKE '%john%' LIMIT 5")
        rules = [i["rule"] for i in res["issues"]]
        self.assertIn("LEADING_WILDCARD_LIKE", rules)

    def test_index_recommender(self):
        query = "SELECT id FROM customers WHERE email = 'test@corp.com' AND age > 21"
        rec = IndexRecommender.recommend(query)
        self.assertEqual(len(rec), 1)
        self.assertIn("idx_customers_email_age", rec[0])

if __name__ == "__main__":
    unittest.main()
