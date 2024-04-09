#!/usr/bin/python
"""Advent of Code 2019, Day 3, Part 1

https://adventofcode.com/2019/day/3

Figure out intersection points of a pair of paths and find minimum manhattan
distance of which point from origin.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

#fn = 'test.dat'
fn = 'wires.dat'

import re

# Convert path to list of coordinates.
def cvt_coords(path):
    coords = []
    x, y = 0, 0
    for p in path:
        dx, dy = { 'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0) }[p[0]]
        for i in range(int(p[1:])):
            coords.append((x := x + dx, y := y + dy))

    return coords

def main():
    # Read in paths
    with open(fn, 'r') as file:
        p1 = file.readline().rstrip("\n").split(',')
        p2 = file.readline().rstrip("\n").split(',')

    # Build list of coordinates for path paths
    c1 = cvt_coords(p1)
    c2 = cvt_coords(p2)

    # Find common coordinate intersections
    common = list(set(c1) & set(c2))

    # Calculate least manhattan distance
    return min([ abs(c[0]) + abs(c[1]) for c in common ])

answer = main()
print(f"Answer is {answer}")
