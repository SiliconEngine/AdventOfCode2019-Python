#!/usr/bin/python
"""Advent of Code 2019, Day 3, Part 2

https://adventofcode.com/2019/day/3

Figure out intersection points of a pair of paths and find minimum distance
to intersecting points from origin.

See test.dat for sample data and wires.dat for full data.

Author: Tim Behrendsen
"""

#fn = 'test.dat'
fn = 'wires.dat'

import re

# Convert path to list of coordinates and also keep a map of
# minimum distance to each point
def cvt_coords(path):
    coords = []
    dist_map = {}
    x, y, dist = 0, 0, 0
    for p in path:
        dx, dy = { 'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0) }[p[0]]
        for i in range(int(p[1:])):
            coords.append((x := x + dx, y := y + dy))
            dist_map[(x, y)] = min(dist_map.get((x, y), 99999999), dist := dist+1)

    return coords, dist_map

def main():
    # Read in paths
    with open(fn, 'r') as file:
        p1 = file.readline().rstrip("\n").split(',')
        p2 = file.readline().rstrip("\n").split(',')

    # Build list of coordinates for path paths
    c1, d1 = cvt_coords(p1)
    c2, d2 = cvt_coords(p2)

    # Find common coordinate intersections
    common = list(set(c1) & set(c2))

    # Calculate least total distance to common point
    return min([ d1[c] + d2[c] for c in common ])

answer = main()
print(f"Answer is {answer}")
