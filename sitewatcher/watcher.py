"""Watches and alerts about missing elements on webpages"""
import itertools
import logging
import os
from typing import Sequence
import unittest

from pkg_resources import resource_stream  # type: ignore
from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore
from selenium.webdriver.remote.webelement import WebElement  # type: ignore
import selenium.common.exceptions as selex  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
import yaml  # type: ignore

from sitewatcher.urls import View


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
        # load view and timestamp data
        with resource_stream('sitewatcher.resources', "views.yaml") as views_fp:
            cls.views = yaml.load(views_fp, yaml.Loader)

    @classmethod
    def tearDownClass(cls):
        # do not close browser if in GUI mode / not headless
        if cls.browser and not cls.gui:
            cls.browser.close()

    def test_views(self):
        for view in self.views:
            with self.subTest(view=view.name):
                self.watch_view(view)

    def wait_for_element(self, xpath: str, timeout=10, panic=True,
                         clickable=False) -> WebElement:
        try:
            if clickable:
                cond = EC.element_to_be_clickable((By.XPATH, xpath))
            else:
                cond = EC.presence_of_element_located((By.XPATH, xpath))
            return WebDriverWait(self.browser, timeout).until(cond)
        except selex.TimeoutException:
            if panic:
                self.fail("Timeout waiting for timestamp to appear")

    def watch_view(self, view: View) -> None:
        timestamps = view.timestamps
        if not timestamps:
            return  # nothing to check
        if view.login:
            # login not supported yet
            logger.debug("Skipping views %s (login only)", view.name)
            return
        url = view.example_url()
        logger.debug("Loading %s ...", url)
        self.browser.get(url)
        with self.assertRaises(selex.NoSuchElementException, msg="404"):
            self.browser.find_element_by_css_selector('img[alt~="404"]')
        self.assertEqual(self.browser.current_url, url, "Loaded url differs")

        # look for each timestamp based on its xpath
        for tsp in timestamps:
            if not tsp.is_active():
                # skipping no longer active timestamps
                continue
            if tsp.login:
                # login not supported yet
                logger.debug("Skipping ts %s (login only)", tsp.name)
                continue
            logger.debug("Searching %s ...", tsp.name)
            with self.subTest(timestamp=tsp.name):
                if tsp.prepare:
                    tsp.prepare(self.browser)
                if tsp.trigger:
                    for trig in tsp.trigger:
                        trig_elem = self.wait_for_element(trig, clickable=True)
                        trig_elem.click()
                self.wait_for_element(tsp.xpath, panic=False)
                els: Sequence[WebElement] = self.browser.find_elements(
                    By.XPATH, tsp.xpath)
                n_els = len(els)
                if n_els == 0 and (alt_xpaths := tsp.alt_xpaths()):
                    for alt_xpath in alt_xpaths:
                        self.wait_for_element(alt_xpath, panic=False)
                        els = self.browser.find_elements(By.XPATH, alt_xpath)
                        n_els = len(els)
                        if n_els > 0:
                            break  # found an alt match
                self.assertGreater(n_els, 0, "Timestamp not found")
                if not tsp.multiple:
                    self.assertEqual(n_els, 1, "Multiple timestamps found")
            logger.debug("Successfully found %s on %s (n=%d)",
                         tsp.name, view.name, len(els))

        # look for unexpected, uncatalogued timestamps
        time_elements = self.browser.find_elements(
            By.CSS_SELECTOR,
            "time-ago, relative-time, local-time"
        )
        found_xpaths = set(map(get_xpath, time_elements))
        def filter_timeelements(path: str) -> bool:
            return any((
                path.endswith("/TIME-AGO"),
                path.endswith("/RELATIVE-TIME"),
                path.endswith("/LOCAL-TIME"),
            ))
        expected = set(filter(filter_timeelements,
                              itertools.chain.from_iterable(
            # only expect time-elements, no custom timestamps in spans
            ts.all_xpaths_rel() for ts in view.timestamps
            if ts.is_active()
        )))
        for found in found_xpaths:
            self.assertIn(found, expected, msg="Unexpected timestamps")


def get_xpath(elem: WebElement, top="body") -> str:
    """Build basic XPath from elem up to given top element"""
    if elem.tag_name.lower() == top:
        return elem.tag_name.upper()
    return (get_xpath(elem.find_element_by_xpath(".."), top) +
            "/" + elem.tag_name.upper())


main = unittest.main  # for cli entry


if __name__ == "__main__":
    main()
