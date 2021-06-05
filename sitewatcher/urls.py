"""GitHub View/URL classifier"""
from collections import defaultdict
from dataclasses import dataclass, field
import enum
import functools
import re
from typing import Any, Dict, List, Sequence


GH = "https://github.com"
EXAMPLE_USER = "EMPRI-DEVOPS"
EXAMPLE_REPO = f"{EXAMPLE_USER}/timestamp-study-watcher"


class ViewType(enum.Enum):
    """Type of GitHub site view."""
    BASE = 1
    REPO = 1


@dataclass
class View():
    """Site view as defined by a url pattern."""
    name: str
    template: str
    regex: str = ""
    example_params: List[Any] = field(default_factory=list)
    type: ViewType = ViewType.REPO

    @property
    def pattern(self) -> re.Pattern:
        return re.compile(self.regex)

    @property
    def example_url(self) -> str:
        return self._urljoin(
            GH,
            EXAMPLE_REPO if self.type is ViewType.REPO else "",
            self.template.format(*self.example_params),
        )

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


URLS = (
  View("root", "/", r"^/?$", type=ViewType.BASE),
  View("user", "/{}", r"^/([^/]+)/?$", [EXAMPLE_USER], type=ViewType.BASE),
  View("compare", "/compare/{}/", r"^/compare/([^/]+)/?$"),  # TODO
  View("commits", "/commits" ,r"^/commits/?"),
  View("commit", "/commit/{}", r"^/commit/([0-9a-f]+)/?$",
       ["550e5b76bf6cbc7c80e27ba3b2e34a12b390179a"]),
  View("issuelist", "/issues", r"^/issues/?$"),
  View("issue", "/issues/{}", r"^/issues/(\d+)/?$", [1]),
  View("labellist", "/labels", r"^/labels/?$"),
  View("label", "/labels/{}", r"^/labels/(\w+)/?$", ["invalid"]),
  View("milestonelist", "/milestone", r"^/milestones/?$"),
  View("milestonelistfilter", "/milestone/{}",
       r"^/milestones/([^/]+)/?$", ["Test"]),
  View("milestone", "/milestone/{}", r"^/milestone/(\d+)/?$", [1]),
  View("pulllist", "/pulls", r"^/pulls/?$"),
  View("pull", "/pull/{}", r"^/pull/(\d+)/?$", [3]),
  View("pullcommits", "/pull/{}/commits/", r"^/pull/(\d+)/commits/?$", [3]),
  View("pullcommit", "/pull/{}/commits/{}",
       r"^/pull/(\d+)/commits/([0-9a-f]+)/?$",
       [3, "aaa7943bac1a5d458d1d0d6773075631b04c0e9b"]),
  View("pullchecks", "/pull/{}/checks", r"^/pull/(\d+)/checks/?$", [3]),
  View("repo", "/", r"^/?$"),
  View("releaselist", "/releases", r"^/releases/?$"),
  View("release", "/releases/tag/{}", r"^/releases/tag/([^/]+)/?$", []),
  View("taglist", "/tags", r"^/tags/?$"),
  View("tree", r"^/tree/"),  # TODO
)
URL_MAP = {url.name: url for url in URLS}


@dataclass
class TS():
    """Timestamp type located by XPath"""
    name: str
    _xpath: str
    multiple: bool = False

    @property
    def xpath(self) -> str:
        """A searchable XPath."""
        if not self._xpath.startswith("/"):
            return "//" + self._xpath
        return self._xpath


TIMESTAMPS: Dict[str, Sequence[TS]] = defaultdict(tuple, {
    # pylint: disable=line-too-long
    "repo": (
        TS("last", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME"),
        TS("file", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/TIME-AGO", True),
    ),
    "commits": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/OL/LI/DIV/DIV/DIV/RELATIVE-TIME", True),
    ),
    "commit": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
    ),
    "issuelist": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "issue": (
        TS("opened", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("origpost", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME"),
        TS("comment", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME", True),
        # action: assignments, closing, labels, milestones, commit references,
        # (all tested)...
        TS("action", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME", True),
    ),
    "pulllist": (
        TS("pr", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "pull": (
        # same as for 'issue'
        TS("opened", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("origpost", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME"),
        TS("comment", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME", True),
        # action: assignments, closing, labels, milestones, commit references,
        # (all tested)...
        TS("action", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME", True),
    ),
    "pullcommits": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/OL/LI/DIV/DIV/DIV/RELATIVE-TIME", True),
    ),
    "pullcommit": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
    ),
    "labellist": (),  # no timestamps
    "label": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "milestonelist": (
        TS("lastupdate", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/UL/LI/DIV/DIV/SPAN/TIME-AGO", True),
    ),
    "milestonelistfilter": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "milestone": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/FORM/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
})
