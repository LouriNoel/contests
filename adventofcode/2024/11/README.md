# AOC 2024/11

## Star 1

Naively do the operations on each stone to build the next iteration.

- If the number is 0, then it becomes 1.
- Else If it has an even number of digits, then the number is split in two numbers evenly (left and right part).
- Else the number is multiplied by 2024.

## Star 2

This does not scale up.

For the second star, we proceed recursively, returning the number of stones originating from a given number
after X iterations ("blinks").

We must also memorize the intermediary results, so we can prevent computing them again.

Note: the order of the stones is meaningless.
