import unittest
from collections import defaultdict
from typing import *

from pkg_resources import resource_stream  # type: ignore
import yaml

import sitewatcher.urls as urls


URLS: List[urls.View] = []


def load_views() -> List[urls.View]:
    with resource_stream('sitewatcher.resources', "views.yaml") as views_fp:
        return yaml.load(views_fp, yaml.Loader)


def setUpModule():
    URLS = load_views()


class XPathUniquenessTest(unittest.TestCase):
    """Check if two timestamps have the same xpath in a view."""
    def test_xpath_uniqueness(self) -> None:
        for view in URLS:
            with self.subTest(view=view.name):
                self._find_view_xpath_duplicates(view)

    def _find_view_xpath_duplicates(self, view: urls.View) -> None:
        seen: Dict[str, List[str]] = defaultdict(list)
        for tsp in view.timestamps:
            seen[tsp.xpath_rel].append(tsp.name)
        for xpath, occurances in seen.items():
            with self.subTest(xpath=xpath):
                if len(occurances) > 1:
                    self.fail(msg=" ".join(occurances))


class PatternMatchTest(unittest.TestCase):
    """Check if the view patterns match the view examples."""
    def test_regex_match(self) -> None:
        for view in URLS:
            match = view.pattern.search(view.example_url(suffix_only=True))
            msg = f"Pattern mismatch for {view.name}"
            with self.subTest(view=view.name):
                self.assertIsNotNone(match, msg=msg)


if __name__ == "__main__":
    unittest.main()
