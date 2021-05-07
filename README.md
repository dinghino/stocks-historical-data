# :monkey: stonks-o-fetcher

A Simple modular tool to fetch and parse data related to the stock market.

[![Build Status](https://travis-ci.com/dinghino/stocks-historical-data.svg?branch=master)](https://travis-ci.com/dinghino/stocks-historical-data)
[![codecov](https://codecov.io/gh/dinghino/stocks-historical-data/branch/master/graph/badge.svg?token=04GQOGJF2R)](https://codecov.io/gh/dinghino/stocks-historical-data)

# Getting started
For the moment the only source is this repository, so to get the program you have to clone it locally.

## Requirements
`Python >3.6`

The program is tested only on a linux environment (WSL 1 and debian) but should
technically work on windows too I think.

## Installation
After cloning and entering the root of the project

```bash
pip install .
```

If you are not on `python 3`
```bash
python3 -m pip install .
```

# Usage

This will make the program available on your system with the command
```
stonks [cli|run]
```
Without any command it will just show you the help.

## `cli` command

Launches the interactive menu to set up your settings.
You can provide an additional option to specify a settings file with

```
stonks cli -f PATH_TO_SETTINGS_FILE
```

If the file exists it will be loaded. If it does not you'll start with an empty
configuration and, on exit, it will save it to your specified path to be later
used.

From here you can change settings and run the app to perform the data scraping.

### Setting up your output path
Like with all the paths you can setup you can use the [unix notation](https://github.com/dinghino/stocks-historical-data#special-characters-in-path)
to shortcut to the current directory or your home directory.

In addition to this you **can** also specify a filename by appending it to the
path with the `.csv` or `.txt` extension, but **it is highly recommended not to**
Since there is no validation on existing files for now, so your data will be overwritten
every time you run the scraper. This could be the desired behaviour in some cases though,
so you have the option to do so.

### Navigating the menu
* Move around with `arrow keys` or `vim keys`.
* Enter a menu or confirm with `Enter`.
* On multi select menus you select with `space` and confirm with `Enter`.
  This will also select the item under the cursor.
* Go back with `ESC`. If on the main menu this will quit **without saving**


## `run` command

This is meant to quickly run an already valid settings file, specifically done
to setup automations through cron jobs or other bash scripts or whatnot.

```
stonks run PATH_TO_SETTINGS_FILE [-s date|last] [-e date|today] -v[vv]
```

* `-s`/`--start-date` Allows you to override **and update** the start date
of the settings.
* `-e`/`--end-date` Allows to override **and update** the end date.
* `-v`/`--verbose` By default the `run` command doesn't produce any output. You
can increase its verbosity level up to 3.

### Start and end dates keywords
For semplicity you can pass special words to the `run` arguments to easily update
the call
* Using `today` for your `--end-date` will, as the word implies, set the end
date to the current date.
* Using `last` on your `--start-date` will set the star date as the day
after the previously set end date.

### Verbosity levels
* **1** shows the progress bar - this should be the default call when running manually
to be able to see what's going on. Also shows the output folder of your files,
In case you're not sure where the files go.
* **2** allows you to see all the settings AND the progress.
* **3** shows some debugging information and logs while loading and running

## Special characters in paths

You can prepend the paths with `.` to point to your local folder, or with `~` for
your current user home directory.
This works both when launching the app and while settings your directories.

```
$ stonks cli -f ./settings/my-settings.json
$ stonks cli -f ~/stonks/settings/my-settings.json
```


# Contributing

If you have an idea for a new data source feel free to add a [related issue](https://github.com/dinghino/stocks-historical-data/issues/new?assignees=dinghino&labels=source+suggestion&template=data-source-request.md&title=). For any other problem
or suggestion feel free to open an issue before opening a PR

To help expand the project you can take a look at the [wiki](https://github.com/dinghino/stocks-historical-data/wiki).

# License
[MIT](./license)
