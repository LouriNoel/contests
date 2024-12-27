# AOC 2024/10

For each trailhead `0` on the grid, compute all the paths (= hiking trails) leading to a `9` recursively.

## Star 1

Group all paths (= hiking trails) by their starting point (= trailhead),
while ignoring duplicate ends / multiple paths leading to the same end.

The score of a trailhead is the number of distinct reachable ending positions.
Sum all these scores to get the result.

## Star 2

We have previously computed all the paths (= hiking trails), so we just need to count them instead of computing ratings.
