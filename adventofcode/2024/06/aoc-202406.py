import os
import sys

from utils.sylis import read

star = int(sys.argv[1]) if len(sys.argv) == 2 else 0
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input")

lines = read(filepath)

DIRS = ["^", ">", "v", "<"]  # ordered: next direction (%4) is a right turn
INCRS = {
    "^": (0, -1),  # dx, dy
    ">": (+1, 0),
    "v": (0, +1),
    "<": (-1, 0)
}


def move_straight(walls: list[tuple[int, int]], W: int, H: int, x0: int, y0: int, d: str) -> tuple[int, int, int, int]:
    """ Return the segment when moving straight from (x0, y0) towards `d`
    until the guard hits a wall or goes OOB (will stop on the last free cell).
    """
    x, y = x0, y0
    dx, dy = INCRS[d]
    while 0 <= x+dx < W and 0 <= y+dy < H and (x+dx, y+dy) not in walls:
        x, y = x+dx, y+dy
    return x0, y0, x, y

def move_from_wall(walls: list[tuple[int, int]], W: int, H: int, wx: int, wy: int) -> list[tuple[str, tuple[int, int, int, int]]]:
    """ Try moving straight from each side of the wall at (wx, wy)
    towards the right (as if the guard hits the wall at the start)
    and until they hit a wall or goes OOB (will stop on the last free cell).

    Return the tuple (direction, segment).
    """
    result = []
    for side, (dx, dy) in INCRS.items():
        x0, y0 = wx+dx, wy+dy
        if 0 <= x0 < W and 0 <= y0 < H and (x0, y0) not in walls:
            d = DIRS[(DIRS.index(side) - 1) % 4]  # left from the wall = right from the opposite
            result.append((d, move_straight(walls, W, H, x0, y0, d)))
    return result

def previous_position(wx: int, wy: int, d: str) -> tuple[int, int, str]:
    """ When hitting the wall at (wx,wy), return the position at the side of the wall, and prepare to turn right. """
    # previous position, and turn right
    right = (DIRS.index(d) + 1) % 4
    opposite = (DIRS.index(d) + 2) % 4
    dx, dy = INCRS[DIRS[opposite]]
    return wx+dx, wy+dy, DIRS[right]


# Instead of computing each cell of the guard's path everytime,
# we pre-compute each segment between the side of a wall (a "hit spot") and another wall/OOB after having turned right.
# Each segment begins after hitting a wall (and turning right) and then ends just before hitting another wall or going OOB.

W, H = len(lines[0]), len(lines)
guard = None  # (x, y, d)
walls = []  # [(x, y)]
segments = {  # d -> [(x1, y1, x2, y2)] start to end
    "^": [],
    ">": [],
    "v": [],
    "<": []
}

# Find walls and the guard
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "#":
            walls.append((x, y))
        if c in DIRS:
            guard = (x, y, c)

# Compute segments after hitting any wall, potentially one per side (if the starting position is free)
for wx, wy in walls:
    wall_moves = move_from_wall(walls, W, H, wx, wy)
    for d, seg in wall_moves:
        segments[d].append(seg)

# Compute the guard's segment (straight line from starting position)
guard_segment = move_straight(walls, W, H, guard[0], guard[1], guard[2])

# Make the guard walk its path a first time until they leave the area
path_segments = [guard_segment]
d = guard[2]
while True:
    last = path_segments[-1]

    # Turn right at the end of the path
    d = DIRS[(DIRS.index(d) + 1) % 4]

    # Check if any segment starts at the ending position of the last segment (and go towards the proper direction)
    new = [s for s in segments[d] if (s[0], s[1]) == (last[2], last[3])]
    if len(new) == 0:
        # No segment was found, so the guard goes OOB. That's the end of the path.
        break
    path_segments.append(new[0])

# Compute the original path and all unique positions
path: list[tuple[int, int, str]] = []  # in order, each visited position AFTER the start (with the direction of the first encounter)
candidates: set[tuple[int, int]] = set()  # unique visited positions
d = guard[2]
for seg in path_segments:
    x, y = seg[0], seg[1]
    dx, dy = INCRS[d]

    candidates.add((x, y))

    while x != seg[2] or y != seg[3]:  # walk on the segment
        x, y = x+dx, y+dy

        if (x, y) not in candidates:
            path.append((x, y, d))  # save the first time this position is reached
        candidates.add((x, y))

    d = DIRS[(DIRS.index(d) + 1) % 4]  # turn right after each segment

if star != 2:
    print(f" *:{len(candidates)}")


if star != 1:
    # 1. The initial position (x0,y0) is not required to be part of a loop
    # 2. An obstacle is only useful when placed on the original path (to make it deviate)
    # 3. Do not walk through the original path everytime an obstacle is tried, that would be a lot of useless iterations

    # We cannot place an obstacle on the guard's initial position
    path = [(x, y, d) for x, y, d in path if (x, y) != (guard[0], guard[1])]
    candidates.remove((guard[0], guard[1]))

    nb_loops = 0
    for wx, wy, d0 in path:
        # Try to place an obstacle at each position on the original path of the guard, then search for a loop.
        # Each position in `path` also have a direction, which can be reversed to find the previous position (on the side),
        # where no wall could have been.

        # Add the wall
        walls.append((wx, wy))

        # Compute the segments to add which start from the sides of the wall.
        # Storage is done as (direction, segment) for both addition and removal.
        added_segments = move_from_wall(walls, W, H, wx, wy)
        removed_segments = []

        # Starting segment, when hitting the wall on our path the first time
        x, y, dr = previous_position(wx, wy, d0)  # start just before the newly placed obstacle, with right turn
        start_segment = [seg[1] for seg in added_segments if seg[0] == dr][0]

        # Find which segments are broken by the new wall, remember to remove them,
        # compute new segments (from the start to the new wall)
        for d, li in segments.items():
            dx, dy = INCRS[d]
            for i in range(len(li)):
                x1, y1, x2, y2 = li[i]  # WARNING : (x1,y1) can be below / on the right of (x2,y2)
                if min(x1,x2) <= wx <= max(x1,x2) and min(y1,y2) <= wy <= max(y1,y2):
                    removed_segments.append((d, (x1, y1, x2, y2)))
                    if (wx, wy) != (x1, y1):
                        added_segments.append((d, (x1, y1, wx-dx, wy-dy)))

        # Temporarily add/remove segments
        for d, seg in removed_segments:
            segments[d].remove(seg)
        for d, seg in added_segments:
            segments[d].append(seg)

        # Walk the new path, starting from the side of the new wall, until the guard ends up in a loop or OOB.
        # Remember each segment of the path: the loop starts when the guard walks on a segment they already visited.
        path_segments = [start_segment]
        d = dr
        while True:
            last = path_segments[-1]

            d = DIRS[(DIRS.index(d) + 1) % 4]  # turn right after each segment
            new = [s for s in segments[d] if (s[0], s[1]) == (last[2], last[3])]
            if len(new) == 0:
                break
            if new[0] in path_segments:
                nb_loops += 1
                print(f"[DEBUG] loop found! nb={nb_loops} wx={wx} wy={wy} d0={d0}")
                break
            path_segments.append(new[0])

        # Undo modifications for the next try
        for d, seg in added_segments:
            segments[d].remove(seg)
        for d, seg in removed_segments:
            segments[d].append(seg)
        walls.remove((wx, wy))

    print(f"**:{nb_loops}")
