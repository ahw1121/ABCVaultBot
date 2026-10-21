import unittest
from pathlib import Path

from abcvaultbot.parser import parse_products, title_matches_keywords

FIXTURE = Path(__file__).resolve().parents[1] / "tmp_shop.html"


class ParserTests(unittest.TestCase):
    def test_parse_products_from_shop_fixture(self) -> None:
        if not FIXTURE.exists():
            self.skipTest("tmp_shop.html fixture not present")
        html = FIXTURE.read_text(encoding="utf-8")
        products = parse_products(html)
        self.assertGreater(len(products), 10)
        makers = [p for p in products if "Maker" in p.title]
        self.assertTrue(makers)
        self.assertEqual(makers[0].sku, "598205")
        self.assertEqual(makers[0].product_id, 56913)

    def test_keyword_match_any(self) -> None:
        self.assertTrue(
            title_matches_keywords(
                "Old Forester Birthday Bourbon", ["birthday", "blanton"]
            )
        )
        self.assertFalse(title_matches_keywords("Maker's Mark", ["blanton"]))


if __name__ == "__main__":
    unittest.main()
