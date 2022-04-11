"""Timestamp model"""
from dataclasses import dataclass, field
from datetime import date
from typing import Callable, List, Optional, Tuple

from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore
import yaml  # type: ignore


@dataclass(frozen=True)
class TS(yaml.YAMLObject):
    """Timestamp type located by XPath"""
    yaml_tag = "!TS"
    name: str
    xpath_rel: str
    multiple: bool = False
    trigger: List[str] = field(default_factory=list)
    prepare: Optional[Callable[[WebDriver], None]] = None
    login: bool = False
    until: Optional[date] = None
    elem_variation: List[str] = field(default_factory=list)
    previous: List[Tuple[str, date]] = field(default_factory=list)

    @property
    def xpath(self) -> str:
        """A searchable XPath."""
        return self._get_searchable_xpath(self.xpath_rel)

    @staticmethod
    def _get_searchable_xpath(path: str) -> str:
        if not path.startswith("/"):
            return "//" + path
        return path

    def alt_xpaths(self) -> List[str]:
        return list(map(self._get_searchable_xpath,
                        self.alt_xpaths_rel()))

    def alt_xpaths_rel(self) -> List[str]:
        return [
            self._replace_elem(self.xpath_rel, alt)
            for alt in self.elem_variation
        ]

    def all_xpaths_rel(self) -> List[str]:
        return [self.xpath_rel] + self.alt_xpaths_rel()

    @staticmethod
    def _replace_elem(xpath: str, elem: str) -> str:
        return "/".join(xpath.split("/")[:-1] + [elem])

    def is_active(self):
        return self.until is None
