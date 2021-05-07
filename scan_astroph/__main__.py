import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from . import __version__
from .config import (Config, configfile_default_location, file_editor,
                     find_configfile, load_config_legacy_format)
from .entry_evaluation import evaluate_entries, sort_entries
from .output import print_entries
from .parse import parse_html
from .tools import load_html

ARXIV_BASE = 'https://arxiv.org/list/astro-ph.EP'


def parse_cli_arguments() -> tuple:
    """Definition and parsing of command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("--config", metavar="/path/to/config",
                        help="Path to configuration file (check README for defaults)")
    parser.add_argument("--default-config", nargs="?", default=False, const=True, metavar="/path/to/config",
                        help="Write default config to default location (or specified path)")
    parser.add_argument("--config-convert", nargs="?", default=False, const=True, metavar="/path/to/config",
                        help="Convert authors and keywords config from legacy format")
    parser.add_argument("--edit", action="store_true",
                        help="Edit config in default text editor")
    parser.add_argument("-d", "--date", default=None,
                        help='date in format yyyy-mm, or "new", or "recent"')
    parser.add_argument("-l", "--len", dest="length", type=int, default=None,
                        help="length of result list, all is -1")
    parser.add_argument("-v", "--rating", type=int, default=None,
                        help="minimum rating for result list")
    parser.add_argument("--reverse", action="store_false", default=None,
                        help="reverse list (lowest ranked paper on top)")
    parser.add_argument("--show-resubmissions", action="store_true", default=None,
                        help="Include resubmissions")
    parser.add_argument("--ignore-cross-lists", action="store_true", default=None,
                        help="Include cross-lists")
    parser.add_argument("--log", choices=["info", "debug"], default="warning",
                        help="Set loglevel")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(__version__))

    return parser.parse_args()


def main():
    args = parse_cli_arguments()

    logging.basicConfig(level=getattr(logging, args.log.upper()))

    # write default config
    if args.default_config:
        if args.default_config is True:
            path = configfile_default_location(mkdir=True)
        else:
            path = args.default_config
        config = Config()
        config.write(path)
        print("Written default config to {}".format(path))
        sys.exit()

    # convert legacy config into new format
    if args.config_convert:
        if args.config_convert is True:
            path = configfile_default_location(mkdir=True)
        else:
            path = args.config_convert
        config = load_config_legacy_format("keywords.txt", "authors.txt")
        config.write(path)
        print("Convert legacy configuration to {}".format(path))
        sys.exit()

    # Open config file in text editor
    if args.edit:
        try:
            path = find_configfile()
        except FileNotFoundError:
            if input("No config file found. Create at default location? [y/N] ").lower() == "y":
                path = configfile_default_location(mkdir=True)
                Config().write(path)
            else:
                print("No file to edit. Exiting")
                sys.exit(1)
        file_editor(path)

    # read config
    config = Config()
    if args.config:
        configfile = args.config
    else:
        try:
            configfile = find_configfile()
        except FileNotFoundError:
            logging.error("Cannot find config file. Check Readme for configuration locations")
            sys.exit(1)

    config.read(configfile)
    logging.info("Reading configuration from file '%s'", configfile)

    # overwrite config from CLI arguments
    config["date"] = args.date
    config["length"] = args.length
    config["minimum_rating"] = args.rating
    config["reverse_list"] = args.reverse
    config["show_resubmissions"] = args.show_resubmissions
    config["show_cross_lists"] = (
        not args.ignore_cross_lists if args.ignore_cross_lists is not None else None
    )

    # parse date string
    if config["date"] == "new" or config["date"] is None:
        address = '{base:s}/new'.format(base=ARXIV_BASE)
        print("querying authors and titles for new submissions (today's listing)")
    elif config["date"] == "recent":
        address = '{base:s}/recent'.format(base=ARXIV_BASE)
        print('querying authors and titles for recent submissions')
    else:
        year, month = args.date.split('-')
        year = year[2:4] if len(year) == 4 else year
        address = '{base:s}/{year:2.2s}{month:2.2s}?show=3000'.format(
                base=ARXIV_BASE, year=year, month=month)
        print('querying authors and titles for listings in {:2.2s}/{:2.2s}'.format(month, year))

    data = load_html(address)

    entries = parse_html(
        data,
        cross_lists=config["show_cross_lists"],
        resubmissions=config["show_resubmissions"],
    )
    evaluate_entries(
        entries, keyword_ratings=config.keywords, author_ratings=config.authors
    )
    entries = sort_entries(
        entries,
        rating_min=config["minimum_rating"],
        reverse=config["reverse_list"],
        length=config["length"],
    )
    print_entries(entries)


if __name__ == "__main__":
    main()
