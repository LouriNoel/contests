import os
import sys
from math import floor, log10
from collections.abc import Callable

from utils.sylis import read, numbers

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

# Should appear in this order to raise `acc` quickly and possibly reach the `acc > target` condition
CONCAT = ("||", lambda a, b: a*(10**(floor(log10(b)) + 1)) + b)
MULTIPLY = ("*", lambda a, b: a * b)
ADD = ("+", lambda a, b: a + b)

binary_operators = [MULTIPLY, ADD]
ternary_operators = [CONCAT, MULTIPLY, ADD]


def check_rec(
        operators: list[tuple[str, Callable[[int, int], int]]],
        target: int,
        operands: list[int],
        acc: int,
        solution: list[tuple[str, int]]
    ) -> bool:
    """ Recursively check to find a solution.

    :param operators: list of allowed operators (to try in that order): tuple (string repr, lambda(acc, operand))
    :param target: target score to obtain
    :param operands: operands left to use (in that order)
    :param acc: cumulative result of previous iterations
    :param solution: holds the solution, list of tuples (operator, operand)
    :return: True if a solution is found (bubbles all the way up), False otherwise.
    """
    if len(operands) == 0:
        return target == acc
    elif acc > target:
        # The input does not have any 0, so acc increases with each step (unless it's "* 1" so ok)
        # So once `acc` goes over the target, it's too late
        return False

    for rep, op in operators:
        solution.append((rep, operands[0]))
        if check_rec(operators, target, operands[1:], op(acc, operands[0]), solution):
            return True
        solution.pop()
    return False

equations = [((nb := numbers(line))[0], nb[1:]) for line in lines]
rejected_equations = []

result = 0
for target, operands in equations:
    solution = [("=", operands[0])]
    if check_rec(binary_operators, target, operands[1:], operands[0], solution):
        print(str(target) + "".join(f" {a} {b}" for a, b in solution))
        result += target
    else:
        rejected_equations.append((target, operands))

if star != 2:
    print(f" *: {result}")

if star != 1:
    for target, operands in rejected_equations:
        solution = [("=", operands[0])]
        if check_rec(ternary_operators, target, operands[1:], operands[0], solution):
            print(str(target) + "".join(f" {a} {b}" for a, b in solution))
            result += target

    print(f"**: {result}")
