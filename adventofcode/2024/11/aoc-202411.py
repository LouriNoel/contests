import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

stones = numbers(lines[0])

def naive(stones: list[int], blink: int) -> int:
    """ Compute every stone at each iteration. """
    # too slow for star 2
    for _ in range(blink):
        next_stones = []
        for stone in stones:
            if stone == 0:
                next_stones.append(1)
            elif (n := len(s := str(stone))) % 2 == 0:
                next_stones.append(int(s[:n//2]))
                next_stones.append(int(s[n//2:]))
            else:
                next_stones.append(stone * 2024)
        stones = next_stones
    return len(stones)


def rec(stone: int, blink: int, seen: dict[tuple[int, int], int]) -> int:
    if blink == 0:
        return 1

    # Memoization is necessary here
    # Number of stones originating from "number" when there are "blink" iterations left
    if (stone, blink) in seen:
        return seen[(stone, blink)]

    if stone == 0:
        count = rec(1, blink-1, seen)
    elif (n := len(s := str(stone))) % 2 == 0:
        count = rec(int(s[:n//2]), blink-1, seen)
        count += rec(int(s[n//2:]), blink-1, seen)
    else:
        count = rec(stone * 2024, blink-1, seen)

    seen[(stone, blink)] = count
    return count


if star != 2:
    result = naive(stones, 25)
    print(f" *: {result}")

if star != 1:
    result = 0
    seen = {}  # (stone, blink) -> count
    for stone in stones:
        result += rec(stone, 75, seen)
    print(f"**: {result}")
