import os
import re
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

src = "".join(lines)

# use regex with grouping to retrieve the values easily
pattern = re.compile(r"mul\((\d+),(\d+)\)")

if star != 2:
    matches = re.findall(pattern, src)
    result = sum(int(a)*int(b) for a, b in matches)
    print(f" *: {result}")

if star != 1:
    src = "do()" + src  # enable at beginning
    dont_clauses = src.split("don't()")

    # only keep enabled parts
    enabled_src = "#".join(clause[i:] if (i := clause.find("do()")) != -1 else "" for clause in dont_clauses)

    result = sum(int(a) * int(b) for a, b in re.findall(pattern, enabled_src))
    print(f"**: {result}")
