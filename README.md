# Contests

This repository contains my libraries and submissions to contests:

- [Advent Of Code](https://adventofcode.com/)

I personally use Ubuntu, so this repository may require little adjustments for others to use.

## Template

Use the `template` branch if you want to start from a clean repository with none of my submissions.

The `utils/sylis.py` file is included in the template. This single file will hold every reusable function.

## AOC

The `adventofcode` directory contains the submissions to AOC, grouped by year, each day having its own subdirectory.

Its `.gitignore` file prevents you from commiting files whose name contains:

- `puzzle`: the puzzle text, in case you need an offline version
- `input`: your input file
- `example`: the puzzle's examples, or your examples
- `output`: output your program could produce
- `log`: logs your program could produce

You can have a `README.md` file for each day to explain your solution.

Copy and rename the file `adventofcode/template.py` into the day's directory,
and start writing.

### Run the code

Place your `input` file alongside your script in the day's directory.
Then run the script directly from PyCharm.

Otherwise from the terminal, go to the root of the repository and execute the script like in this example: `python3 -m adventofcode.2024.01.aoc-202401`

## Miscellaneous

### Time an execution

Use the `time` command:

```
time python3 -m adventofcode.2024.01.aoc-202401

# verbose
/usr/bin/time -v python3 -m adventofcode.2024.01.aoc-202401
```
