#!/usr/bin/python
"""Advent of Code 2019, Day 10, Part 2

https://adventofcode.com/2019/day/10

Given a map of "asteroids", figure out which asteroid has the most
asteroids in sight, without one occluding another (at same angle).
From there, start destroying asteroids one at a time with a laser
starting directly straight up in a circle. Compute which asteroid will
be the 200th one destroyed (after removing ones in the way).

See test.dat for test data and asteroids.dat for full data.

Author: Tim Behrendsen
"""

import re
import math

fn = 'test2.dat'
fn = 'asteroids.dat'

# Convert to polar coordinates
def cartesian_to_polar(x, y):
    # Calculate the distance from the origin to the point (r)
    r = math.sqrt(x**2 + y**2)

    # Calculate the angle in radians and convert to degrees
    theta = math.degrees(math.atan2(y, x))

    # Make angle range 0-360, 0 = straight up, then make it an integer
    # to avoid floating point errors
    a = round(theta, 5) + 90
    if a < 0:
        a += 360
    return round(r, 5), int(a * 100)

def main():
    asteroids = []
    y = 0
    with open(fn, 'r') as file:
        for line in file:
            asteroids += [ (item[0], y) for item in enumerate(line) if item[1] == '#' ]
            y += 1

    # First find the point that can see the most rays. At that point,
    # save off the list of coordinates and their angles.
    highest_count = 0
    high_coords = []

    for test_x, test_y in asteroids:
        # Calculate polar coordinates of asteroids relative to us
        pcoords = []
        for ax, ay in asteroids:
            if ax == test_x and ay == test_y:
                continue            # Skip ourself
            r, theta = cartesian_to_polar(ax - test_x, ay - test_y)
            pcoords.append((r, theta, ax, ay))

        # Count number of unique angles
        count = len(set([ c[1] for c in pcoords ]))

        # Keep track of best
        if count > highest_count:
            highest_count = count
            high_coords = pcoords.copy()

    # Sort the list of coordinates by the angle, then by distance
    high_coords.sort(key=lambda item: (item[1], item[0]))

    # Scan list of coordinates in order of angle, and only count an
    # angle once. Keep track of ones that we've counted, then count
    # further ones as we go back through. Stop at #200.
    chk = set()
    count = 0
    while True:
        last_angle = None
        for c in high_coords:
            if c in chk:
                continue
            if last_angle != None and last_angle == c[1]:
                continue
            last_angle = c[1]
            chk.add(c)

            if (count := count + 1) == 200:
                # Answer is x * 100 + y
                return c[2] * 100 + c[3]

answer = main()
print(f"Answer is {answer}")
