# AOC 2024/05

Parse the input file and retrieve the rules and updates separately.

Find the index of an update's middle page by dividing its number of pages by 2 (rounded down).

## Star 1

Find the number of updates having the correct order.

For each update, check every rule `a|b` where pages `a` and `b` are part of the update.
The update is in order if `index(a) < index(b)` everytime.

## Star 2

For each update that is not in order, reorder its pages according to all rules until it gets in order.
