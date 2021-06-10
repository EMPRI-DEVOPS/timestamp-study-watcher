"""Watches and alerts about missing elements on webpages"""
import logging
import os
from typing import Sequence
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sitewatcher.urls import URL_MAP, TIMESTAMPS, View


logger = logging.getLogger("watcher")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class SiteWatcherTest(unittest.TestCase):
    browser: WebDriver
    gui: bool

    @classmethod
    def setUpClass(cls):
        options = webdriver.FirefoxOptions()
        cls.gui = bool(os.environ.get("SITEWATCHER_GUI", None))
        options.headless = not cls.gui
        cls.browser = webdriver.Firefox(options=options)

    @classmethod
    def tearDownClass(cls):
        # do not close browser if in GUI mode / not headless
        if cls.browser and not cls.gui:
            cls.browser.close()

    def test_views(self):
        for name, view in URL_MAP.items():
            with self.subTest(view=name):
                self.watch_view(view)

    def wait_for_element(self, xpath: str, timeout=10):
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)),
            )
        except selex.TimeoutException:
            self.fail("Timeout waiting for timestamp to appear")

    def watch_view(self, view: View) -> None:
        timestamps = TIMESTAMPS[view.name]
        if not timestamps:
            return  # nothing to check
        url = view.example_url()
        logger.debug("Loading %s ...", url)
        self.browser.get(url)
        with self.assertRaises(selex.NoSuchElementException, msg="404"):
            self.browser.find_element_by_css_selector('img[alt~="404"]')
        self.assertEqual(self.browser.current_url, url, "Loaded url differs")

        # look for each timestamp based on its xpath
        for tsp in timestamps:
            logger.debug("Searching %s ...", tsp.name)
            with self.subTest(timestamp=tsp.name):
                self.wait_for_element(tsp.xpath)
                els: Sequence[WebElement] = self.browser.find_elements_by_xpath(tsp.xpath)
                n_els = len(els)
                self.assertGreater(n_els, 0, "Timestamp not found")
                if not tsp.multiple:
                    self.assertEqual(n_els, 1, "Multiple timestamps found")
            logger.debug("Successfully found %s on %s (n=%d)",
                         tsp.name, view.name, len(els))

        # look for unexpected, uncatalogued timestamps
        time_elements = self.browser.find_elements_by_css_selector(
            "time-ago, relative-time"
        )
        found_xpaths = set(map(get_xpath, time_elements))
        expected = set(
            # only expect time-elements, no custom timestamps in spans
            xpath for xpath in view.timestamp_xpaths
            if xpath.endswith("/TIME-AGO") or xpath.endswith("/RELATIVE-TIME")
        )
        self.assertEqual(found_xpaths, expected,
                         msg="Expected timestamps do not match")


def get_xpath(elem: WebElement, top="body") -> str:
    """Build basic XPath from elem up to given top element"""
    if elem.tag_name.lower() == top:
        return elem.tag_name.upper()
    return (get_xpath(elem.find_element_by_xpath(".."), top) +
            "/" + elem.tag_name.upper())


main = unittest.main  # for cli entry


if __name__ == "__main__":
    main()
