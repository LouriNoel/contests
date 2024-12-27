# AOC 2024/09

Process the input file as a single line.

## Star 1

For each digit of the input:

- if its index is even, then it is a file
- if its index is odd, then it is free space

Uncompress the input: for each digit `n`, if it is a file then add its id `n` times to the blocks list,
otherwise it is free space so add `-1` (reserved id for free space) `n` times to the blocks list.

Be careful: the file ids can go beyond 9, so we must store them in a list.

```python
uncompressed = []
next_id = 0
for kind, digit in enumerate(disk_map):
    if kind % 2 == 0:  # file
        uncompressed.extend([next_id]*int(digit))
        next_id += 1
    else:  # free space
        uncompressed.extend([-1]*int(digit))
```

Now remember two indexes: one at the beginning and the other at the end of the block list.
Starting from the end, move each file block to the first free space at the beginning
by swapping ids and updating the start and end indexes.
You can stop when the start index becomes greater than the end index.

Compute the checksum.

## Star 2

We will need another strategy because it is tedious
to move up to 9 blocks of file ids, and checking if there is enough space for them.

Parse the input into a list of chunks `(length, id)` (either files or free spaces).

Starting from the end of the list, for each file,
check if there is enough free space (starting from the beginning) at a lower index.
When found, we cannot simply swap these chunks because there can be more free space: we need to split it.

A file can only be moved once, so either we remember the id of all files that were moved,
or we only move files of decreasing id.

Computing the checksum requires a different formula.
