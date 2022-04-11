"""View data"""
from typing import List
from sitewatcher.urls import View, ViewType, EXAMPLE_ORG, EXAMPLE_USER

from .timestamps_data import TIMESTAMPS


def add_timestamps(views: List[View]) -> List[View]:
    """Fuse timestamp data with view data"""
    for view in views:
        if not view.timestamps:
            view.timestamps = list(TIMESTAMPS[view.name])
    return views


URLS = add_timestamps([
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
       [3, "68534b440024f4f919da7f6a3f6709a836779fa6"]),
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
  View("jobrun", "/runs/{}", r"^/runs/(\d+)/?$", [3586294909]),
  View("projectlist", "/projects", r"^/projects/?$"),
  View("project", "/projects/{}", r"^/projects/(\d+)/?$", [2]),
])
