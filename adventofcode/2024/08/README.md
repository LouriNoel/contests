# AOC 2024/08

Find all the antennas and group them by frequency.

For each pair `(x1,y1)` and `(x2,y2)` of antennas of the same frequency,
compute the difference `dx = x2 - x1` and `dy = y2 - y1`.

Beware of bounds checking when placing antinodes.

## Star 1

Place an antinode on each side of a pair of antennas, at `(x1-dx, y1-dy)` and `(x2+dx, y2+dy)`

## Star 2

Now do it repetitively until the bounds are reached.

For `i` and `j` starting at `0` (because there is now an antinode at each antenna position,
if the antenna is part of a pair), place an antinode at `(x1-i*dx, y1-i*dy)` and `(x2+j*dx, y2+j*dy)`
