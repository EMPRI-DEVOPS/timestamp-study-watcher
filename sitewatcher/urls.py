# pylint: disable=missing-function-docstring
"""GitHub View/URL classifier"""
from dataclasses import dataclass, field
from datetime import date
import enum
import functools
import re
from typing import Any, Dict, List, Optional, Sequence


GH = "https://github.com"
EXAMPLE_USER = "cburkert"
EXAMPLE_ORG = "EMPRI-DEVOPS"
EXAMPLE_REPO = f"{EXAMPLE_ORG}/timestamp-study-watcher"


class ViewType(enum.Enum):
    """Type of GitHub site view."""
    BASE = 0
    REPO = 1


@dataclass
class View():
    """Site view as defined by a url pattern."""
    name: str
    template: str
    regex: str = ""
    example_params: List[Any] = field(default_factory=list)
    type: ViewType = ViewType.REPO
    login: bool = False

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
    def timestamps(self) -> Sequence['TS']:
        return TIMESTAMPS[self.name]

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


URLS = (
  View("root", "/", r"^/?$", type=ViewType.BASE),  # dashboard if logged in
  View("userissues", "/issues", r"^/issues/?$", type=ViewType.BASE, login=True),
  View("userpulls", "/pulls", r"^/pulls/?$", type=ViewType.BASE, login=True),
  View("user", "/{}", r"^/([^/]+)/?$", [EXAMPLE_USER], type=ViewType.BASE),
  View("orgrepos", "/orgs/{}/repositories", r"^/orgs/([^/]+)/repositories/?$",
       [EXAMPLE_ORG], type=ViewType.BASE),
  View("compare", "/compare/{}", r"^/compare/([^/]+)/?$", ["main...testpull"]),
  View("commits", "/commits" ,r"^/commits/?"),
  View("commit", "/commit/{}", r"^/commit/([0-9a-f]+)/?$",
       ["550e5b76bf6cbc7c80e27ba3b2e34a12b390179a"]),
  View("issuelist", "/issues", r"^/issues/?$"),
  View("issue", "/issues/{}", r"^/issues/(\d+)/?$", [1]),
  View("labellist", "/labels", r"^/labels/?$"),
  View("label", "/labels/{}", r"^/labels/(\w+)/?$", ["invalid"]),
  View("milestonelist", "/milestones", r"^/milestones/?$"),
  View("milestonelistfilter", "/milestones/{}",
       r"^/milestones/([^/]+)/?$", ["Test"]),
  View("milestone", "/milestone/{}", r"^/milestone/(\d+)/?$", [1]),
  View("pulllist", "/pulls", r"^/pulls/?$"),
  View("pull", "/pull/{}", r"^/pull/(\d+)/?$", [3]),
  View("pullcommits", "/pull/{}/commits/", r"^/pull/(\d+)/commits/?$", [3]),
  View("pullcommit", "/pull/{}/commits/{}",
       r"^/pull/(\d+)/commits/([0-9a-f]+)/?$",
       [3, "5604c7abee3d6813c02902700964b96ac8ac6c0e"]),
  View("pullchecks", "/pull/{}/checks", r"^/pull/(\d+)/checks/?$", [3]),
  View("repo", "/", r"^/?$"),
  View("releaselist", "/releases", r"^/releases/?$"),
  View("release", "/releases/tag/{}", r"^/releases/tag/([^/]+)/?$",
       ["demo"]),
  View("taglist", "/tags", r"^/tags/?$"),
  View("treeroot", "/tree/{}", r"^/tree/([^/]+)/?$", ["main"]),
  View("treesub", "/tree/{}/{}", r"^/tree/([^/]+)/(.+)$",
       ["main", "sitewatcher"]),
  View("blob", "/blob/{}/{}", r"^/blob/([^/]+)/(.+)$",
       ["main", "sitewatcher/watcher.py"]),
  View("wikipage", "/wiki/{}", r"^/wiki(/[^/]+)/?$", ["Another-page"]),
  View("wikipagehistory", "/wiki/{}/_history", r"^/wiki/([^/]+)/_history$",
       ["Another-page"]),
  View("wikipagerev", "/wiki/{}/{}", r"^/wiki/([^/]+)/([0-9a-f]+)/?$",
       ["Home", "cd27fb08b2fdff5995aada4f2adec8a260a30564"]),
  View("workflowruns", "/actions", r"^/actions(/workflows/[^/]+)?/?$"),
  View("workflowrun", "/actions/runs/{}", r"^/actions/runs/(\d+)/?$",
       [917858452]),
  View("jobrun", "/runs/{}", r"^/runs/(\d+)/?$", [2772535510]),
  View("projectlist", "/projects", r"^/projects/?$"),
  View("project", "/projects/{}", r"^/projects/(\d+)/?$", [2]),
)
URL_MAP = {url.name: url for url in URLS}


@dataclass(frozen=True)
class TS():
    """Timestamp type located by XPath"""
    name: str
    xpath_rel: str
    multiple: bool = False
    trigger: List[str] = field(default_factory=list)
    login: bool = False
    until: Optional[date] = None
    elem_variation: List[str] = field(default_factory=list)

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


TIMESTAMPS: Dict[str, Sequence[TS]] = {
    # pylint: disable=line-too-long
    "root": (),  # TODO need to be logged in to see dashboard
    "user": (
        TS("repolast", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/UL/LI/DIV/SPAN/RELATIVE-TIME", True,
           until=date(2021, 8, 6)),  # disappeared from the repo list in overview
        # ... but it is still shown on the repositories tab of user
        # but for orgs it is not a tab but a separate url (see orgrepos)
        TS("repolistrepolast", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/DIV/DIV/RELATIVE-TIME", True,
           trigger=['/html/body/div[4]/main/div[1]/div/div/div[2]/div/nav/a[2]'])
    ),
    "orgrepos": (
        TS("repolast", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "userissues": (
        TS("issuechanged", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True, login=True),
    ),
    "userpulls": (
        TS("pullchanged", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True, login=True),
    ),
    "repo": (
        TS("last", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME"),
        TS("file", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/TIME-AGO", True),
    ),
    "treeroot": (
        # same as 'repo' if we are in the root path '/tree/<ref>/'
        TS("last_root", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME"),
        TS("file_root", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/TIME-AGO", True),
    ),
    "treesub": (
        # ... different if we are in a subdirectory
        TS("last", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME"),
        TS("file", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/TIME-AGO", True),
    ),
    "blob": (
        TS("last", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/SPAN/RELATIVE-TIME"),
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
        TS("opened-stickyheader", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("origpost", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME"),
        TS("comment", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME", True),
        # issue action: assignments, closing, labels, milestones, commit references,
        # (all tested)...
        TS("issueaction", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME", True),
    ),
    "pulllist": (
        TS("pr", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "pull": (
        # similar to 'issue'
        # exceptions: no opened date, different paths for comment and action,
        # origpost and commit are identical
        TS("origpost", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME"),
        TS("comment", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/H3/A/RELATIVE-TIME", True),
        # PR action: assignments, closing, labels, milestones, commit references,
        # (all tested)...
        TS("praction",
           "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME",
           True, elem_variation=["TIME-AGO"]),
        # sometimes praction are returned with a time-ago element (A-B testing?)
        # BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/TIME-AGO
    ),
    "pullcommits": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/OL/LI/DIV/DIV/DIV/RELATIVE-TIME", True),
    ),
    "pullcommit": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("commitdropdown", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/DIV/A/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "pullchecks": (
        TS("commitdropdown", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/A/DIV/SPAN/RELATIVE-TIME", True),
        TS("commitdropdown-stickyheader", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/A/DIV/SPAN/RELATIVE-TIME", True),
        TS("buildcompleted", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/SECTION/DIV/DIV/DIV/SPAN/SPAN/RELATIVE-TIME"),
    ),
    "labellist": (),  # no timestamps
    "label": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "milestonelist": (
        # GH serves the lastupdate TS as a span, not a time-element,
        # our extension turns it into a time-ago
        #TS("lastupdate", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/UL/LI/DIV/DIV/SPAN/TIME-AGO", True),
        TS("lastupdate", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/UL/LI/DIV/DIV/SPAN/SPAN", True),
    ),
    "milestonelistfilter": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "milestone": (
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/FORM/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
    ),
    "taglist": (
        TS("tag", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/RELATIVE-TIME", True),
    ),
    "releaselist": (
        TS("release", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", True),
        # position of hidden date (legacy)
        TS("release-legacy", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/RELATIVE-TIME", True),
    ),
    "release": (
        TS("tag", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/P/RELATIVE-TIME"),
    ),
    "compare": (
        # apperently no commits here, not even for the listed commits
    ),
    "wikipage": (
        TS("created", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
    ),
    "wikipagerev": (
        # same as wikipage
        TS("created", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
    ),
    "wikipagehistory": (
        TS("committed", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/FORM/DIV/UL/LI/DIV/DIV/RELATIVE-TIME", True),
    ),
    "workflowruns": (
        TS("triggered", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", True),
        # the view contains a second however hidden start timestamp (probably legacy)
        TS("triggered-legacy", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", True),
    ),
    "workflowrun": (
        TS("triggered", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO"),
    ),
    "jobrun": (
        TS("finished", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/SECTION/DIV/DIV/DIV/SPAN/SPAN/RELATIVE-TIME"),
    ),
    "projectlist": (
        TS("projectupdated", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", True),
    ),
    "project": (
        TS("lastupdated", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/BUTTON/SPAN/RELATIVE-TIME"),
        # Activity list is dynamically loaded when clicking on 'Menu'
        TS("activity", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/P/SPAN/RELATIVE-TIME", True,
           trigger=['/html/body/div[4]/div/main/div[2]/div/div[4]/div[1]/div[3]/div[3]/button']),
    ),
}
