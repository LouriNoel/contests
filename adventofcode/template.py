import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

# TODO functions definition and common processing

if star != 2:
    pass  # TODO star 1

if star != 1:
    pass  # TODO star 2
