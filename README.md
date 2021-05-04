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

## Usage and first teps
After cloning and entering the root of the project

```bash
pip install .
```

If you are not on `python 3`
```bash
python3 -m pip install .
```

This will make the program available on your system with the command 
```
stonks-cli
```
On first startup you'll have to setup your settings, **especially** the `output path`.

There is some validation for fields, so if something is missing you'll see it.

You can use the default `~` to point the path to your home folder, so you can
set the path to something like `~/stonks/` or whatever you like.

If you define a filename in your path, meaning that it ends with either `.csv` or `.txt`
that's the filename it will use to output the data, otherwise the filename will be
generated automatically from the settings.

> ### :warning: File checking
> There is not check on existing files yet, and that's on purpose, so
> if you specify a custom file name it will be overwritten at every execution.
> 
> It is recommended to **not** specify a filename and let the program do its thing.
> It is also **strongly** suggested to actually change te path to something familiar.

### Controls
The important things are esplained in the program itself, and are mostly out of
my control due dependecies, but:

* Menu navigation: `arrow keys` and `vim bindings`
* Confirm a value: `Enter`
* Multiselect when available `Space` - also `enter` will add the currently
 highlighted entry
* Exit from an input field with no defaults: type an `empty space` then `enter`
* With default values you can press `enter` to confirm it.

> ### :warning: Saving your settings
> Exiting the application with `ESC` will NOT save your settings. you have to
> use the main menu option to do so.

### CLI and automation
As of version `0.6.0` the only way to use this program is through the interactive
cli menus, but i'm planning on adding the option to launch it with arguments to automate
the execution of the process, specify all the required paramenters through arguments
and handle different settings files to easily automate the execution through multiple settings.

# Contributing
A proper documentation will come later, but here's the gist if you want to contribute on new
features.

## Components
The project is meant to be easily expandable and flexible. There are two main type of components to
consider:

* Source components
  * Fetchers
  * Parsers
* Writer components

The name are pretty self explanatory I think.

The whole system is already setup to be almost completely automated
Each `source handler` is included in its own module (folder). The module, through
the `__init__.py` **has** to export some values:

* `Fetcher` - your fetcher class, inheriting from `FetcherBase`
* `Parser` - your parser class, inheriting from `ParserBase`
* `source` - `string.` Unique value identifying the source handled, can be everyhing
* `friendly_name` - `string`. The text that appears on the CLI
* `description` - `string` a brief description of the source. appears in the cli.

`Writers` are similar, but instead of `Fetcher` and `Parser` and `source` they must have:

* `Writer` - your writer class, inheriting from `WriterBase`
* `output_type` - `string` unique identifier for the class.

The rest of the attributes remain the same.

> :information_source: You can look at the existing modules inside `stonks/components` to better understand

There's a `manager` component that is already set up to import all the valid modules from the
`components/handlers` and `components/writers` folders, so when your module is ready it should work.
Loading is done in the cli module, so that the app is actually empty by itself.

> For a module to be valid it has to have the required `classes` and at least the `source`/`output_type`

## Custom formatting
If you take a look at the existing components `description` you'll notice some strange formatting.

The CLI has a custom formatter - because i like colored crayons - to ease highlighing important words.
Instead of the standard `string.format` that replaces the values, here we wrap the words into `{}` to
specify formatting.

```python
#  {word:color}
#  {word:style}
#  {word:color|style}
text = 'This {word:blue} is blue!'
# > this word is blue! - with `word` in blue.
```

Formatting is done through [termcolor](https://pypi.org/project/termcolor/), so valid values
are the ones in their documentation.

As before, check existing modules to better understand.

> :warning: String content
> For the moment there are a few issues with the default implementation of `string.format`
> that catches various character, specifically the `.` and `:` that is used as our delimiter, for now
> Inserting these character in a block to format will cause problems.
>
> As a rule of thumb, if you write your description and when testing the cli the page doesn't
> load, it means that there's probably something wrong with the text there.

### Testing
Testing is important. There is an `utils` file with a bunch of function and a `decorator` class,
used mainly as container for the functions.
Most of the tests require at least one decorator if they are not testing for failures.

### Pull Requests
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. I'm trying to follow git flow specs to some degree, so eventually the PR toward `develop` please.

:warning: Please make sure to update tests as appropriate.

## License
[MIT](./license)
