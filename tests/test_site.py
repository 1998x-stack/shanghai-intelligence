"""Smoke tests for data-driven pages; no network, no external dependencies."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site


class TestShanghaiSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_site.build()

    def test_taxonomy(self):
        self.assertEqual(len(build_site.TOPICS), 7)
        self.assertEqual(len(build_site.DISTRICTS), 16)

    def test_all_topic_and_district_pages_are_generated(self):
        for topic in build_site.TOPICS:
            self.assertTrue((build_site.OUT / "topics" / topic["id"] / "index.html").exists())
        for district in build_site.DISTRICTS:
            self.assertTrue((build_site.OUT / "districts" / district["id"] / "index.html").exists())

    def test_required_routes(self):
        for path in ("index.html", "archive/index.html", "daily/index.html",
                     "topics/index.html", "districts/index.html",
                     "reports/index.html", "monthly/index.html", "monthly/2026-10/index.html", "sources/index.html", "404.html", "feed.json"):
            self.assertTrue((build_site.OUT / path).is_file(), path)

    def test_draft_is_not_public(self):
        events = build_site.load_events()
        self.assertTrue(all(x["status"] == "verified" for x in events))
        self.assertFalse((build_site.OUT / "events" / "example-hongkou-teacher-2027" / "index.html").exists())

    def test_links_include_project_base(self):
        home = (build_site.OUT / "index.html").read_text(encoding="utf-8")
        self.assertIn('/shanghai-intelligence/assets/site.css', home)
        self.assertIn('/shanghai-intelligence/topics/jobs/', home)
        self.assertIn("招聘与编制", home)
        self.assertIn("活动与生活", home)

    def test_october_month_archiving(self):
        page = (build_site.OUT / "monthly/2026-10/index.html").read_text(encoding="utf-8")
        self.assertIn("2026-10", page)
        self.assertIn("sh-oct2026-ai-manufacturing-plan", page)
        self.assertIn("october-2026-shanghai-intelligence", page)

    def test_feed_is_array(self):
        data = json.loads((build_site.OUT / "feed.json").read_text(encoding="utf-8"))
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
