import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

disk_map = "".join(lines)

# list of file parts (nb blocks, id) in order. id = -1 for free space.
memory: list[tuple[int, int]] = []

# lay out memory
next_id = 0
for kind, digit in enumerate(disk_map):
    if kind % 2 == 0:  # file
        memory.append((int(digit), next_id))
        next_id += 1
    else:  # free space
        memory.append((int(digit), -1))


def checksum(memory: list[tuple[int, int]]) -> int:
    result = 0
    pos = 0
    for space, idt in memory:
        if idt != -1:  # only use files
            result += sum(p for p in range(pos, pos + space)) * idt
        pos += space
    return result


def failed_defragmentation(disk_map: str) -> list[tuple[int, int]]:
    uncompressed: list[int] = []

    next_id = 0
    for kind, digit in enumerate(disk_map):
        if kind % 2 == 0:  # file
            uncompressed.extend([next_id]*int(digit))
            next_id += 1
        else:  # free space
            uncompressed.extend([-1]*int(digit))

    # "bubble"-sort
    start, end = 0, len(uncompressed)-1
    while start < end:
        if uncompressed[start] == -1:  # free space
            while uncompressed[end] == -1:  # find next ending file block to move
                end -= 1
            if start < end:
                uncompressed[start], uncompressed[end] = uncompressed[end], uncompressed[start]
            end -= 1
        start += 1

    memory_li: list[list[int]] = []
    for idt in uncompressed:
        if len(memory_li) > 0 and memory_li[-1][1] == idt:
            memory_li[-1][0] += 1
        else:
            memory_li.append([1, idt])
    memory = [(li[0], li[1]) for li in memory_li]

    return memory


def successful_defragmentation(memory: list[tuple[int, int]]) -> list[tuple[int, int]]:
    previous_file_id = max(t[1] for t in memory) + 1
    for end in range(len(memory)-1, -1, -1):
        file_s, file_i = memory[end]
        if file_i != -1 and file_i < previous_file_id:  # find next file to move
            previous_file_id = file_i
            for start in range(0, end):
                free_s, free_i = memory[start]
                # find next free-space block that could fit the file
                if free_i == -1 and free_s >= file_s:
                    delta = free_s - file_s
                    memory[end] = (file_s, -1)
                    memory[start] = (file_s, file_i)
                    if delta != 0:
                        memory.insert(start + 1, (delta, -1))
                        # end += 1  # useless, otherwise next time it will check the newly placed free-block first
                    break
    return memory

if star != 2:
    fragmented_memory = failed_defragmentation(disk_map)
    print(f" *: {checksum(fragmented_memory)}")

if star != 1:
    organized_memory = successful_defragmentation([t for t in memory])
    print(f"**: {checksum(organized_memory)}")
