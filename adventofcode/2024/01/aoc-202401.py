import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

# Build the left and right list (numbers at even / odd indexes, in the order they appear in the input file)
locations = numbers(" ".join(lines))
left, right = locations[::2], locations[1::2]

if star != 2:
    # Sort each list so we can pair up the smallest / 2nd smallest / etc. number of each of them
    left.sort()
    right.sort()

    # Sum the distance of each pair (numbers associated by "smallest" rank)
    total_distance = sum(abs(a - b) for a, b in zip(left, right))
    print(f" *: {total_distance}")

if star != 1:
    # Sum all the similarity scores (unique number in left list * its number of occurrences in the right list)
    similarity = sum(x * right.count(x) for x in set(left))
    print(f"**: {similarity}")
