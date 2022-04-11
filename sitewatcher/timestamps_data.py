"""Timestamp data"""
from datetime import date
from typing import Dict, Tuple

from . import utils
from .timestamps import TS


TIMESTAMPS: Dict[str, Tuple[TS, ...]] = {
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
        TS("practionpush",
           "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/RELATIVE-TIME",
           #"BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/A/TIME-AGO",
           True, elem_variation=["TIME-AGO"]),  # ... this one as well
    ),
    "pullcommits": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/OL/LI/DIV/DIV/DIV/RELATIVE-TIME", True),
    ),
    "pullcommit": (
        TS("commit", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIFF-FILE-FILTER/DIFF-LAYOUT/DIV/DIV/DIV/RELATIVE-TIME",
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIFF-FILE-FILTER/DIV/DIV/DIV/RELATIVE-TIME", date(2022, 2, 17)),
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", date(2022, 1, 17)),
           ],
        ),
        TS("commitdropdown", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIFF-FILE-FILTER/DIFF-LAYOUT/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/DIV/A/DIV/SPAN/RELATIVE-TIME", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIFF-FILE-FILTER/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/DIV/A/DIV/SPAN/RELATIVE-TIME", date(2022, 2, 17)),
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/DIV/A/DIV/SPAN/RELATIVE-TIME", date(2022, 1, 17)),
           ],
        ),
    ),
    "pullchecks": (
        TS("commitdropdown", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/A/DIV/SPAN/RELATIVE-TIME", True,
           trigger=["/html/body/div[4]/div/main/div[2]/div/div/div[4]/div[1]/div[1]/div/div/details"]),
        TS("commitdropdown-stickyheader", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DETAILS/DETAILS-MENU/DIV/A/DIV/SPAN/RELATIVE-TIME", True,
           trigger=["/html/body/div[4]/div/main/div[2]/div/div/div[4]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/details"],
           prepare=utils.shrink_and_scroll_down),
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
        TS("tag", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/RELATIVE-TIME", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/RELATIVE-TIME", date(2021, 10, 26)),
           ]),
    ),
    "releaselist": (
        TS("release", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/LOCAL-TIME", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", date(2021, 11, 28)),
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/RELATIVE-TIME", date(2021, 10, 26)),
           ]),
        # position of hidden date (legacy)
        TS("release-legacy", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/RELATIVE-TIME", True,
           until=date(2021, 10, 26)),
    ),
    "release": (
        TS("tag", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/LOCAL-TIME",
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", date(2021, 11, 28)),
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/P/RELATIVE-TIME", date(2021, 10, 26)),
           ],
        ),
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
        TS("triggered", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", date(2021, 10, 29)),
           ]),
        # the view contains a second however hidden start timestamp (probably legacy)
        TS("triggered-legacy", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO", date(2021, 10, 29)),
           ]),
    ),
    "workflowrun": (
        TS("triggered", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/SPAN/TIME-AGO"),
    ),
    "jobrun": (
        TS("finished", "BODY/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/SECTION/DIV/DIV/DIV/SPAN/SPAN/RELATIVE-TIME"),
    ),
    "projectlist": (
        TS("projectupdated", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", True,
           previous=[
               ("BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME", date(2021, 12, 16)),
           ]),
    ),
    "project": (
        TS("lastupdated", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/DIV/RELATIVE-TIME"),
        TS("issue", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/DIV/BUTTON/SPAN/RELATIVE-TIME"),
        # Activity list is dynamically loaded when clicking on 'Menu'
        TS("activity", "BODY/DIV/DIV/MAIN/DIV/DIV/DIV/DIV/DIV/DIV/UL/LI/P/SPAN/RELATIVE-TIME", True,
           trigger=['/html/body/div[4]/div/main/div[2]/div/div[4]/div[1]/div[3]/div[3]/button']),
    ),
}
