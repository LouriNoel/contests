import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

rules = []
updates = []
for line in lines:
    if "|" in line:
        a, b = line.split("|")
        rules.append((int(a), int(b)))
    elif line != "":
        updates.append([int(i) for i in line.split(",")])

result_ordered = 0
result_non_ordered = 0
for update in updates:
    candidate = True

    subrules = [(x, y) for x, y in rules if x in update and y in update]
    for x, y in subrules:
        if not (update.index(x) < update.index(y)):
            candidate = False
            break

    if candidate:
        result_ordered += update[len(update)//2]  # middle page
    else:  # incorrectly ordered
        changed = True
        while changed:  # reorder until every page stays in place
            changed = False
            for x, y in subrules:
                ix, iy = update.index(x), update.index(y)
                if not (ix < iy):
                    update[ix], update[iy] = update[iy], update[ix]
                    changed = True

        result_non_ordered += update[len(update)//2]  # middle page

print(result_ordered)
print(result_non_ordered)
