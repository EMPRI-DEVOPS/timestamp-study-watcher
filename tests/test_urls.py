import unittest
from collections import defaultdict
from typing import *

import sitewatcher.urls as urls




class XPathUniquenessTest(unittest.TestCase):
    """Check if two timestamps have the same xpath in a view."""
    def test_xpath_uniqueness(self) -> None:
        for view in urls.URLS:
            with self.subTest(view=view.name):
                self._find_view_xpath_duplicates(view)

    def _find_view_xpath_duplicates(self, view: urls.View) -> None:
        seen: Dict[str, List[str]] = defaultdict(list)
        for tsp in view.timestamps:
            seen[tsp._xpath].append(tsp.name)
        for xpath, occurances in seen.items():
            with self.subTest(xpath=xpath):
                if len(occurances) > 1:
                    self.fail(msg=" ".join(occurances))


class PatternMatchTest(unittest.TestCase):
    """Check if the view patterns match the view examples."""
    def test_regex_match(self) -> None:
        for view in urls.URLS:
            match = view.pattern.search(view.example_url(suffix_only=True))
            msg = f"Pattern mismatch for {view.name}"
            with self.subTest(view=view.name):
                self.assertIsNotNone(match, msg=msg)


if __name__ == "__main__":
    unittest.main()
