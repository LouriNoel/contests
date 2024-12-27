# AOC 2024/07

`||` can be implemented differently in Python. The last once is more efficient:

```python
c = int(f"{a}{b}")
c = a * (10 ** len(f"{b}")) + b

from math import floor, log10
c = a * (10 ** (floor(log10(b)) + 1)) + b
```

## Base Decomposition

The following can be used in Python to get the string representation of some base decompositions of a number `n`: 

```python
# binary
"{0:b}".format(n)
# hexadecimal
"{0:x}".format(n)
# octal
"{0:o}".format(n)
# padding left with zeroes until the provided length is reached
"{0:b}".format(n).zfill(32)
```

Ternary decomposition must be implemented ourselves.

### Star 1

`n` operands must be combined with either `+` or `*` to give a certain result.
That makes `2**(n-1)` possibilities (2 choices made n-1 times because operators go between operands).

For each number between `0` and `2**(n-1)` (excluded), find its binary decomposition on `n-1` digits.
Each `1` is a `*` and each `0` is a `+`. Compute the result and compare it to the target.

### Star 2

There are now 3 operators `||`, `*` and `+`, so there are `3**(n-1)` possibilities.

We can proceed the same way with ternary decompositions, with eah `2` being a `||`.

The program completes in 21s.

## Recursively

A lot of time is lost doing the decomposition and computing the partial result of the same operators.
Using a recursive function instead makes the program completes in a mere 1s.

We can also stop the computation early if the cumulative result goes over the target number.
This is because all operands are strictly positive in the input file, so the cumulative result can only increase.

To make that happen faster, we must choose in priority the operator that is more likely to give a bigger result.
So we must choose  `||`, `*` and then `+` in that order.

```text
9||9 = 99
9*9  = 81
9+9  = 18

2*2 = 4
2+2 = 4

# Only exception
1*1 = 1
1+1 = 2
```
