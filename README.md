scan_astro-ph
=============
Scan abstract listings on ArXiV's astro-ph (or others) for keywords and favorite authors to distill a list of papers most relevant for *you*.
Keywords can be typed in manually or be found by ranking word occurrences in a provided file (e.g., a `.bib` file).

The bulk of the code was created by [Robert Glas](https://github.com/rmglas), with significant contributions by [Simske](https://github.com/Simske).

# Installation
Requirements: Python >3.5

These scripts can be installed with pip:
```
pip install --upgrade git+https://github.com/matiscke/scan_astro-ph.git#egg=scan_astroph
```
Depending on your Python installation, you might need one of the following:
```
pip3 install --upgrade git+https://github.com/matiscke/scan_astro-ph.git#egg=scan_astroph
python3 -m pip install --upgrade git+https://github.com/matiscke/scan_astro-ph.git#egg=scan_astroph
```

# Usage
## Query today's astro-ph listing for relevant papers
First setup your keywords and authors (see configuration section),
then just run `scan_astro-ph` (or `python -m scan_astroph`) to get the relevant listings.

## Command line reference
```
usage: scan_astro-ph [-h] [--config /path/to/config] [--default-config [/path/to/config]] [--config-convert [/path/to/config]] [--edit] [-d DATE] [-l LENGTH] [-v RATING] [--reverse] [--show-resubmissions] [--ignore-cross-lists] [--log {info,debug}] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --config /path/to/config
                        Path to configuration file (check README for defaults)
  --default-config [/path/to/config]
                        Write default config to default location (or specified path)
  --config-convert [/path/to/config]
                        Convert authors and keywords config from legacy format
  --edit                Edit config in default text editor
  -d DATE, --date DATE  date in format yyyy-mm, or "new", or "recent"
  -l LENGTH, --len LENGTH
                        length of result list, all is -1
  -v RATING, --rating RATING
                        minimum rating for result list
  --reverse             reverse list (lowest ranked paper on top)
  --show-resubmissions  Include resubmissions
  --ignore-cross-lists  Include cross-lists
  --log {info,debug}    Set loglevel
  --version             show program's version number and exit
```
# Configuration
In the configuration file all the keywords and authors have to be set, as well as other optional configuration.

The easiest way to get started is to run `scan_astro-ph --edit`, this will open the configuration file in the
default text editor.

Alternatively create a default configfile with `scan_astro-ph --default-config`, and edit it manually.

## Configuration format:
```ini
[authors]
# author = rating
Alpher = 1
Bethe = 2
Gamov = 3

[keywords]
# keyword = rating
star = 1
planet = 2
habitable = 3

[options]
# other optional options (can also be set on CLI)
date = new
length = -1
minimum_rating = 6
reverse_list = False
show_resubmissions = False
show_cross_lists = True
```

## Automatically find keywords with `scan_astro-ph.wordcounter`:
- Run `scan_astro-ph.wordcounter file_to_scan` (or `python -m scan_astroph.wordcounter file_to_scan`).
It scan the text file and extract words with 4-12 characters from it, sorted by occurrence in the file.
- You will be asked to rank these suggested keywords. For each word shown, press 'Enter' to reject it or provide an integer rating, e.g., from 1 to 5 (higher=more relevant). Conclude by pressing `C`.
- Manually insert particularly important authors into the config file (e.g. with `scan_astro-ph --edit`)

## Configuration locations:
`scan_astro-ph` searches the these paths for the config file, and loads the first found:
- from environment variable: `$SCAN_ASTRO_PH_CONF`
- from home directory: `~/.scan_astroph.conf`
- default path (platform dependent):
  - on Linux / Unix (except MacOS): `$XDG_CONFIG_HOME/scan_astroph/scan_astroph.conf` (`XDG_CONFIG_HOME` defaults to `~/.config`)
  - on MacOS: `~/Library/Application Support/scan_astroph/scan_astroph.conf`
  - on Windows: `$HOME/Documents/scan_astroph/scan_astroph.conf`

# Feedback
All feedback, including bug reports, feature requests, pull requests, etc., is welcome. `scan_astro-ph` is being actively developed in an open repository; if you have any trouble please raise an [issue](https://github.com/matiscke/scan_astro-ph/issues/new).

---------------------
License: [CC BY 3.0](http://creativecommons.org/licenses/by/3.0/)
