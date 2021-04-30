# Stonks :monkey:

A Simple tool to fetch and parse data related to the stock market.

## Installation

For now a direct installation is not available.

To develop or use this project you have to clone it in a `Python 3` environment. For the moment
you have two options to launch it:
*  from the root directory of the project with
   ```bash
   python .
   ```
* installing it locally with
  ```bash
  pip install .
  ```
  This will let you call the program with `stonks`.

As of now there are no cli arguments you can pass but I am planning to add some in the future
to allow automation of the scraping process.

> :warning: **If you encounter an error regarding simple-term-menu you are probably trying to install
>  on a Python 2 environment. If that's not the case try to manually install it with**

```
python3 -m pip install simple-term-menu
```

## Usage

Basic usage is pretty straight forward: Navigate through the menus to change your settings and lunch
it from the main menu.

Default output path for the files is in the `./data/output/` directory of the repository, but you
can change it as you like.
If you define a filename in the output path that will be the name of the file containing the data,
otherwise the name will be auto generated from your settings and data.

Your settings are automatically saved when you exit the program.

### :information_source: Output file type

One thing to note is the choice of the output file. You currently have two options:
1. Aggregate File
  Will take all the data available for all the files pulled, extract the desired
  _symbols_ and put everything in a single file. **These files can become quite big** if a huge number
  of symbol is selected and/or a wide date range is. **:warning: This may cause the program to crash**
  so don't be worried and just open an issue it it happens.

2. Ticker Files
  The second choice creates a file for each symbol and strips some columns from the data, depending on the source,
  but always the symbol since - at least in my mind - you should already know what that data is for since it's in
  the filename.

## Contributing

A proper documentation will come later when I've finalized the major aspects to allow easy expansion
of the project, but I'm open to suggestions.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

:warning: Please make sure to update tests as appropriate.

## License
[MIT](./license)
