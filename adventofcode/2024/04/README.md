# AOC 2024/04

I came up with 3 different ways to solve this puzzle.

## Look from a starting point

For a grid of width `W` and height `H`, the `(x,y)` positions are as follows:

- `(0, 0)`: top-left cell of the grid
- `(W-1, 0)`: top-right cell of the grid
- `(0, H-1)`: bottom-left cell of the grid
- `(W-1, H-1)`: bottom-right cell of the grid

Let's define an increment of position for each of the 8 directions:

```python
INCR = [
    (0, -1),  # UP
    (1, -1),  # UP RIGHT
    (1, 0),  # RIGHT
    (1, 1),  # RIGHT DOWN
    (0, 1),  # DOWN
    (-1, 1),  # DOWN LEFT
    (-1, 0),  # LEFT 
    (-1, -1),  # LEFT UP
]
```

### Star 1

For each cell in the grid, if it is an `X`, check in all 8 directions that the next cell is an `M`, then `A` and lastly `S`.
Do not forget to check for bounds.

```python
grid: list[str] | list[list[str]]  # list of rows, or 2D-array of characters
H, W = len(grid), len(grid[0])
result = 0
for y in range(H):  # for each cell (x,y)
    for x in range(W):
        if grid[y][x] == "X":
            for dx, dy in INCR:  # for each direction
                if all(0 <= x+i*dx < W
                       and 0 <= y+i*dy < H
                       and grid[y+i*dy][x+i*dx] == c
                       for i, c in enumerate("XMAS")):
                    result += 1
print(result)
```

### Star 2

For each cell in the grid, if it is an `A`, check the neighbouring diagonal cells.
`MAS` (or in reverse `SAM`) must appear on two diagonals.

To avoid checking for bounds, you can look for an `A` in all cells except those on the border.

```python
grid: list[str] | list[list[str]]  # list of rows, or 2D-array of characters
H, W = len(grid), len(grid[0])
result = 0
for y in range(1, H-1):  # for each cell (x,y) except on borders
    for x in range(1, W-1):
        if grid[y][x] == "A":
            if 2 == sum(1 for dx, dy in INCR[1::2]  # look for M and S in the same diagonal
                        if grid[y-dy][x-dx] == "M" and grid[y+dy][x+dx] == "S"):
                result += 1
print(result)
```

## Find patterns

Write or generate 8 rotations of the XMAS pattern, and 4 rotations of the X-MAS pattern.
Let's keep `.` as a wildcard.

Search for all appearances of these "sub-grid" patterns in the input grid and count them.

```python
grid: list[str] | list[list[str]]  # list of rows, or 2D-array of characters
H, W = len(grid), len(grid[0])
result = 0
for pattern in patterns:  # for each pattern
    h, w = len(pattern), len(pattern[0])
    for y in range(H-h+1):  # for each cell in the grid (also account for the pattern's size)
        for x in range(W-w+1):
            # try to match the pattern from its top-left corner, ignore wildcards
            if all(pattern[dy][dx] == "." 
                   or pattern[dy][dx] == grid[y+dy][x+dx] 
                   for dy in range(h) for dx in range(w)):
                result += 1
print(result)
```

### Star 1 pattern

```python
patterns = [
    ["XMAS"],
    [
        "X...",
        ".M..",
        "..A.",
        "...S",
    ],
    [
        "X",
        "M",
        "A",
        "S",
    ],
    [
        "...X",
        "..M.",
        ".A..",
        "S...",
    ],
    ...
]
```

### Star 2 pattern

```python
patterns = [
    [
        "M.S",
        ".A.",
        "M.S"
    ],
    [
        "M.M",
        ".A.",
        "S.S"
    ],
    [
        "S.M",
        ".A.",
        "S.M"
    ],
    [
        "S.S",
        ".A.",
        "M.M"
    ]
]
```

## Use Regex

Process the input grid as a single line: join each row with an unused EOL placeholder.

Also convert every pattern to a single line: join each row with wildcards.
There must be as many wildcards as the width of the grid (plus the added EOL placeholder).

The EOL placeholder is there to prevent a pattern's row from matching at the line wrap of the grid.
The common EOL character `\n` cannot be used with regex easily, so we better replace it.

Another drawback: a pattern now spans whole multiple lines because of all the wildcards,
so be careful with regex functions that do not allow matches to overlap.
You need to use a function that gives a single match since a provided starting index.

Example: For a grid of width `10` with `1` added wildcard at each EOL,
an X-MAS pattern (of width `3`) could be converted into `M.S.{8}.A..{8}M.S`.
