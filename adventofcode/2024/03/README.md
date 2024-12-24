# AOC 2024/03

Parse the input file and concat every line into a single line.

## Star 1

Use regex to search all appearances of the pattern `mul((\d+),(\d+))` in the input file.
Retrieve the groups, multiply both numbers, and sum it all.

## Star 2

1. Add a `do()` at the beginning of the input, to make sure that following `mul` instructions are enabled.
2. Split the input at each `don't()` instruction.
3. In each part, find the first `do()`: the only enabled instructions are after that.
4. Use regex on these enabled parts
