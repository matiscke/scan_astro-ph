import json
import os.path
from collections import Counter
from re import findall
import argparse
from pathlib import Path

from .config import Config, find_configfile, configfile_default_location


def _count_words(fname):
    with open(fname) as f:
        text = f.read()
    words = findall(r'\b\w{4,12}\b', text.lower())
    return Counter(words)


def most_common_words_in_file(fname, n, verbose=False):
    counts = _count_words(fname)
    if verbose:
        for word, count in [['WORD', 'COUNT']] + counts.most_common(n):
            print(f'{word:>10} {count:>6}')
    return counts


def select_keywords(config: Config, counts):
    """Let the user rate or reject keywords"""
    # sort list by decreasing number of occurrence
    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    print('for each suggested keyword, give a rating from 1 to 5 or reject it by pressing "enter".\nConclude by pressing "C".')

    # don't ask for previously added words
    for key in config.keywords:
        try:
            counts.pop(key)
        except KeyError:
            pass

    for keyword in counts:
        while True:
            # repeat current iteration until a correct input was given
            usr_rating = input('{}: '.format(keyword))
            if (usr_rating == chr(27)) | (usr_rating.lower() == 'c'):
                # escape was pressed
                return config
            elif usr_rating == "":
                break
            else:
                try:
                    config.add_keyword(keyword, int(usr_rating))
                    break
                except ValueError:
                    print('rating must be an integer.')
                    continue
    return config


def main():
    parser = argparse.ArgumentParser("Extract keywords from arbitrary text files")
    parser.add_argument("-c", "--config", help="Config file to write keywords to")
    parser.add_argument("file", help="Text file to scan for keywords")
    args = parser.parse_args()

    config = Config()

    if args.config:
        configfile = args.config
    else:
        try:
            configfile = find_configfile()
        except FileNotFoundError:
            configfile = configfile_default_location(mkdir=True)
    try:
        config.read(configfile)
    except FileNotFoundError:
        pass

    counts = most_common_words_in_file(args.file, 200)
    select_keywords(config, counts)

    print("Writing config back to {}".format(configfile))
    config.write(configfile, overwrite=True)

if __name__ == "__main__":
    main()
