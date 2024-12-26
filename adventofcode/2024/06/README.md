# AOC 2024/06

## Move all the way

Create a function to move from a position in a certain direction.
The guard can go out-of-bounds (OOB) but stays in place and turns right if there is a wall in front of them.
This should return the new position and new direction.

### Star 1

Find the guard's position and direction, and call the move function until they get OOB.

Remember every visited position and count them,
or draw the last direction on the grid at every move and count these at the end instead.

### Star 2

For each empty cell in the grid (no wall and no guard), temporarily place an obstacle and walk the path again
until the guard goes OOB or is stuck in a loop.

Then your program does not complete because you (I?) forgot that the starting point is not necessarily part of the loop.
So we must remember each position (and direction) the guard visits, and check at every step if it is visited again.

The program is still awfully slow... so next optimisation:
an obstacle is useful only if it is placed somewhere on the original path of the guard.
So for each cell in the original path of the guard, temporarily place an obstacle and walk through it all again.

... which still takes roughly 20 or 30 minutes to complete.

So another optimisation kicks in: the guard do not have to start at the same position everytime.
Make them start on the side of the added obstacle.
Choosing the correct side is easy if we remember the direction the guard came in
at the position of the obstacle on the original path.

This takes 2 minutes, but we can do better!

## Precompute segments

When parsing the file, store the position of each wall.

Then for each side of a wall, go straight in the "right" direction until you encounter another wall or go OOB,
as if the guard just hit the wall, turned right, and continued on their path.

So we have precomputed each "segment" from a starting point (side of a wall) to an end in a straight line.
Also compute the segment from the starting position of the guard and the first wall encountered.

### Star 1

Each segment (x1,y1,x2,y2) goes from (x1,y1) to (x2,y2).
The next segment is the one that starts at (x2,y2).

Proceed like this from the starting position of the guard,
until the ending position of the segment is on the border of the grid.

Compute the list of visited cells from the list of segments that compose the path of the guard.

### Star 2

For each visited cell on the original path, place an obstacle.
This will break some segments and add other segments (starting from each of the obstacle's sides).

Computing the new path from the correct side of the obstacle is significantly shorter with segments
than doing it when walking through every cell one at a time.

This now takes 16 seconds to complete.
