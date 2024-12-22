import re

#################
# INPUT PARSING #
#################

def read(path: str) -> list[str]:
    """ Read a file and return the list of lines (without EOL). """
    with open(path, "r") as file:
        lines = [row.rstrip("\r\n") for row in file.readlines()]
    return lines


def digits(src: str) -> list[int]:
    """ Return the list of individual digits contained inside the provided string. """
    return [int(c) for c in src if c.isdigit()]


def numbers(src: str, negative=False) -> list[int]:
    """ Return the list of numbers contained inside the provided string.

    Numbers can be separated by any non-digit character(s).

    If `negative` is True, then minus signs can be part of numbers to make them negative (even "-0").
    Otherwise, all numbers are considered positive (so "1-3" gives `[1, 3]`).
    """
    pattern = r"-?\d+" if negative else r"\d+"
    return [int(m) for m in re.findall(pattern, src)]


def words(src: str, separator: str | None = None) -> list[str]:
    """ Return the list of words (separated by a space) contained inside the provided string.

    Uses the provided separator. By default (`separator` is None), the words are separated by any number of spaces.
    """
    return [w for w in src.split(separator) if w != ""]
