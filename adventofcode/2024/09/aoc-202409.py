import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

disk_map = "".join(lines)


def star1():
    uncompressed = []

    next_id = 0
    for kind, digit in enumerate(disk_map):
        if kind % 2 == 0:  # file
            uncompressed.extend([next_id]*int(digit))
            next_id += 1
        else:  # free space
            uncompressed.extend([-1]*int(digit))

    start, end = 0, len(uncompressed)-1
    while start < end:
        if uncompressed[start] == -1:  # free space
            while uncompressed[end] == -1:  # find next ending file block to move
                end -= 1
            uncompressed[start], uncompressed[end] = uncompressed[end], uncompressed[start]
            end -= 1
        start += 1

    checksum = sum(pos * idt for pos, idt in enumerate(uncompressed) if idt != -1)
    print(f" *: {checksum}")


def star2():
    u: list[tuple[int, int]] = []

    next_id = 0
    for kind, digit in enumerate(disk_map):
        if kind % 2 == 0:  # file
            u.append((int(digit), next_id))
            next_id += 1
        else:  # free space
            u.append((int(digit), -1))

    end = len(u) - 1
    previous_file_id = next_id + 1
    while end > 0:
        file_s, file_i = u[end]
        if file_i != -1 and file_i < previous_file_id:  # find next file to move
            previous_file_id = file_i
            for start in range(0, end):
                free_s, free_i = u[start]
                # find next free-space block that could fit the file
                if free_i == -1 and free_s >= file_s:
                    delta = free_s - file_s
                    u[end] = (file_s, -1)
                    u[start] = (file_s, file_i)
                    if delta != 0:
                        u.insert(start+1, (delta, -1))
                        # end += 1  # useless, otherwise next time it will check the newly placed free-block first
                    break
        end -= 1

    checksum = 0
    pos = 0
    for space, idt in u:
        if idt != -1:
            checksum += sum(p for p in range(pos, pos+space)) * idt
        pos += space
    print(f"**: {checksum}")

if star != 2:
    star1()

if star != 1:
    star2()
