import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

section_separator_index = lines.index("")

rules = [numbers(line) for line in lines[:section_separator_index]]
updates = [numbers(line) for line in lines[section_separator_index+1:]]

ordered_updates = []
unordered_updates = []

for update in updates:
    applicable_rules = [(x, y) for x, y in rules if x in update and y in update]
    for x, y in applicable_rules:
        if not (update.index(x) < update.index(y)):
            unordered_updates.append(update)
            break
    else:
        ordered_updates.append(update)  # all rules are respected, the pages are sorted already


if star != 2:
    # sum of the middle pages
    result = sum(update[len(update)//2] for update in ordered_updates)
    print(f" *: {result}")

if star != 1:
    for update in unordered_updates:
        applicable_rules = [(x, y) for x, y in rules if x in update and y in update]

        changed = True
        while changed:  # reorder until every page stays in place
            changed = False
            for x, y in applicable_rules:
                ix, iy = update.index(x), update.index(y)
                if not (ix < iy):
                    update[ix], update[iy] = update[iy], update[ix]
                    changed = True

    # sum of the middle pages
    result = sum(update[len(update)//2] for update in unordered_updates)
    print(f"**: {result}")
