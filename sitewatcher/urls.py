# pylint: disable=missing-function-docstring
"""GitHub View/URL classifier"""
from dataclasses import dataclass, field
import enum
import functools
import re
from typing import Any, List, Sequence

import yaml  # type: ignore

from .timestamps import TS


GH = "https://github.com"
EXAMPLE_USER = "cburkert"
EXAMPLE_ORG = "EMPRI-DEVOPS"
EXAMPLE_REPO = f"{EXAMPLE_ORG}/timestamp-study-watcher"


class ViewType(enum.Enum):
    """Type of GitHub site view."""
    BASE = "base"
    REPO = "repo"

    @staticmethod
    def representer(dumper: yaml.Dumper, data: 'ViewType'):
        return dumper.represent_scalar('!VIEWTYPE', data.value)

    @classmethod
    def constructor(cls, loader: yaml.Loader, node):
        value = loader.construct_scalar(node)
        return cls(value)


yaml.add_representer(ViewType, ViewType.representer)
yaml.add_constructor('!VIEWTYPE', ViewType.constructor)


@dataclass
class View(yaml.YAMLObject):
    """Site view as defined by a url pattern."""
    yaml_tag = "!VIEW"
    name: str
    template: str
    regex: str = ""
    example_params: List[Any] = field(default_factory=list)
    type: ViewType = ViewType.REPO
    login: bool = False
    timestamps: List[TS] = field(default_factory=list)

    @property
    def pattern(self) -> re.Pattern:
        return re.compile(self.regex)

    def example_url(self, suffix_only=False) -> str:
        suffix = self.template.format(*self.example_params)
        if suffix_only:
            return suffix
        return self._urljoin(
            GH,
            EXAMPLE_REPO if self.type is ViewType.REPO else "",
            suffix,
        )

    @property
    def timestamp_xpaths(self) -> Sequence[str]:
        return [tsp.xpath_rel for tsp in self.timestamps]

    @staticmethod
    def _urljoin(*parts: str) -> str:
        def _join(a: str, b: str) -> str:
            if not a:
                return b
            if not b:
                return a
            if a.endswith("/") and b.startswith("/"):
                return a + b[1:]
            if a.endswith("/") or b.startswith("/"):
                return a + b
            return "/".join((a, b))
        return functools.reduce(_join, parts)
