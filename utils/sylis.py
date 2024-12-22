from collections.abc import Callable
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


########
# GRID #
########

def apply_transform_to_array2d[T: (list, tuple, str)](
        array: list[T],
        transform: Callable[[list[T]], list[T]]
) -> list[T]:
    """ Apply a transformation to a 2d array and ensure the returned result has the same type. """

    if len(array) == 0:
        return []

    trans = transform(array)

    if type(array[0]) == list:
        return [list(row) for row in trans]
    if type(array[0]) == str:
        return ["".join(row) for row in trans]
    if type(array[0]) == tuple:
        return [tuple(row) for row in trans]

    # unknown type
    return trans


def rotate_array2d_clockwise[T: (list, tuple, str)](array: list[T]) -> list[T]:
    """ Rotate a 2d array 90° clockwise. Return a copy without updating the original. """
    # https://stackoverflow.com/a/8421412
    return apply_transform_to_array2d(array, lambda arr: list(zip(*arr[::-1])))


def rotate_array2d_counterclockwise[T: (list, tuple, str)](array: list[T]) -> list[T]:
    """ Rotate a 2d array 90° counterclockwise. Return a copy without updating the original. """
    # https://stackoverflow.com/a/8421412
    return apply_transform_to_array2d(array, lambda arr: list(zip(*arr))[::-1])


def build_wordseek_chunks(word: str, wildcard: str = '.') -> list[list[str]]:
    """ Build 8 chunks from a word, like in a word seek puzzle.
    Include line, column, diagonals, and reversed.

    `wildcard` is used to denote empty spaces.
    """
    if len(word) == 0:
        return []
    if len(word) == 1:
        return [[word]]

    # Build the diagonal chunk
    diagonal = ["".join((letter if x == y else wildcard) for x, letter in enumerate(word)) for y in range(len(word))]

    chunks = [[word], diagonal]

    # Rotate chunks until we have 8 of them
    for _ in range(6):
        chunks.append(rotate_array2d_clockwise(chunks[-2]))

    return chunks


def findall_chunk_in_grid(grid: list[str], chunk: list[str], unused: str = '§') -> list[tuple[int, int]]:
    """ Search all occurrences of a chunk inside a grid.
    Return the list of the (x,y) positions matching the top-left corner of the chunk.

    The origin (0,0) is the top-left corner of the grid, X+ horizontal towards the right, Y+ vertical towards the bottom.
    Matched chunks can overlap.
    The '.' character in a chunk is a wildcard matching any character.
    The `unused` character must be guaranteed to not appear in the chunk (must be different from EOL).

    Regex is used internally, so characters with special meaning (except the wildcard '.')
    must be replaced in the chunk.
    """

    # A chunk can span multiple lines. Both the grid and chunk are flattened to make the search easier with regex.
    # Once flattened, the chunk's rows are joined together, separated by the same count of wildcard characters
    # (corresponding to the difference of width between the grid and chunk).

    # To prevent a single chunk's row from matching against multiple lines of the grid,
    # an `unused` character must be inserted at each EOL (also adding another wildcard between each of the chunk's rows).

    # difference in width
    w, sub_w = len(grid[0]), len(chunk[0])
    dw = w - sub_w
    gap_pattern = ".{" + str(dw + 1) + "}"  # +1 to account for the added separator at each EOL

    matched_indexes = []

    flat_grid = unused.join(grid)
    flat_pattern = re.compile(gap_pattern.join(chunk))

    # A chunk can span multiple lines, so `re.finditer` cannot be used because it does not allow overlapping matches.
    start = 0
    while (m := flat_pattern.search(flat_grid, start)) is not None:
        i = m.start()
        x, y = i % w, i // w  # 1D index -> 2D position
        matched_indexes.append((x, y))
        start = i + 1

    return matched_indexes
