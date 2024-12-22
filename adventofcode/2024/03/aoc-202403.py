import os
import re
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

src = "".join(lines)

pattern = re.compile(r"mul\((\d+),(\d+)\)")
matches = re.findall(pattern, src)

result = sum(int(a)*int(b) for a, b in matches)
print(f" *: {result}")

dont_li = src.split("don't()")
enabled = True
result = sum(int(a)*int(b) for a, b in re.findall(pattern, dont_li[0]))
for dont_part in dont_li[1:]:
    do_li = dont_part.split("do()")
    for do_part in do_li[1:]:
        result += sum(int(a) * int(b) for a, b in re.findall(pattern, do_part))
print(f"**: {result}")
