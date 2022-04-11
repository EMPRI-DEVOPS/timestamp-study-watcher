"""Batch change for div removal on 2022-03-17"""
import argparse
from datetime import date
import yaml

from sitewatcher.urls import View


AFFECTED_VIEWS = [
    'issuelist',
    'issue',
    'label',
    'milestonelist',
    'milestonelistfilter',
    'pulllist',
    'pull',
    'pullcommits',
    'pullchecks',
    'wikipage',
    'wikipagehistory',
    'wikipagerev',
    'jobrun',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r+"),
                        help="File for YAML view/ts data")
    args = parser.parse_args()
    with args.file as yml_fp:
        views = yaml.load(yml_fp, yaml.Loader)
        for view in views:
            if view.name in AFFECTED_VIEWS:
                update_view(view)
        args.file.seek(0)
        args.file.truncate()
        yaml.dump(views, yml_fp)


def update_view(view: View):
    for ts in view.timestamps:
        ts.previous.append((
            ts.xpath_rel, date(2022, 3, 17)
        ))
        ts.xpath_rel = ts.xpath_rel.replace("/MAIN/DIV/", "/MAIN/")



if __name__ == "__main__":
    main()
