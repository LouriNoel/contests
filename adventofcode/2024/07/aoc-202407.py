import os
import sys

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

equations = [((nb := numbers(line))[0], nb[1:]) for line in lines]

binary_equations = []
rejected_equations = []
ternary_equations = []

for target, operands in equations:
    n = len(operands) - 1
    for i in range(0, 2**n):
        s = "{0:b}".format(i).zfill(n)
        r = operands[0]
        dbg = f"{target} = {operands[0]}"
        for e, o in zip(operands[1:], s):
            if o == "0":
                r += e
                dbg += f" + {e}"
            else:
                r *= e
                dbg += f" * {e}"
        if target == r:
            binary_equations.append((target, operands))
            print(dbg)
            break
    else:
        rejected_equations.append((target, operands))

result = sum(target for target, _ in binary_equations)
if star != 2:
    print(f" *: {result}")


# https://stackoverflow.com/a/2267428
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


if star != 1:
    for target, operands in rejected_equations:
        n = len(operands) - 1
        for i in range(0, 3 ** n):
            s = baseN(i, 3).zfill(n)
            r = operands[0]
            dbg = f"{target} = {operands[0]}"
            for e, o in zip(operands[1:], s):
                if o == "0":
                    r += e
                    dbg += f" + {e}"
                elif o == "1":
                    r *= e
                    dbg += f" * {e}"
                else:  # o == "2"
                    r = r * (10 ** len(f"{e}")) + e
                    dbg += f" || {e}"
            if target == r:
                ternary_equations.append((target, operands))
                print(dbg)
                break
    result += sum(target for target, _ in ternary_equations)
    print(f"**: {result}")
