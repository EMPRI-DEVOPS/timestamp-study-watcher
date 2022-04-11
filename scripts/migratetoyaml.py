import argparse
import yaml

from sitewatcher.view_data import URLS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("w+"),
                        help="File for YAML view/ts data")
    args = parser.parse_args()
    with args.file as yml_fp:
        yaml.dump(URLS, yml_fp)
        # test if we can read the identical data back
        args.file.seek(0)
        data = yaml.load(yml_fp, yaml.Loader)
        assert data == URLS


if __name__ == "__main__":
    main()
