import logging
import sys
from typing import Sequence

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .urls import URL_MAP, TIMESTAMPS, View


logger = logging.getLogger("watcher")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def watch_view(browser: WebDriver, view: View) -> None:
    timestamps = TIMESTAMPS[view.name]
    if not timestamps:
        return  # nothing to check
    url = view.example_url
    logger.debug("Loading %s ...", url)
    browser.get(url)
    if browser.current_url != url:
        logger.error("Failed to load %s. Got '%s'", view.name,
                     browser.current_url)
        return
    for tsp in timestamps:
        logger.debug("Searching %s ...", tsp.name)
        els: Sequence[WebElement] = browser.find_elements_by_xpath(tsp.xpath)
        if not els:
            logger.error("Timestamp %s not found on %s", tsp.name, view.name)
        elif not tsp.multiple and len(els) > 1:
            logger.error("Unexpected number of %s found on %s (n=%d)",
                         tsp.name, view.name, len(els))
        else:
            logger.debug("Successfully found %s on %s (n=%d)",
                         tsp.name, view.name, len(els))


def main() -> None:
    options = webdriver.FirefoxOptions()
    options.headless = True
    try:
        browser = webdriver.Firefox(options=options)
        for _name, view in URL_MAP.items():
            watch_view(browser, view)
    except Exception as e:
        logger.exception(e)
    finally:
        if browser:
            browser.close()


if __name__ == "__main__":
    main()
