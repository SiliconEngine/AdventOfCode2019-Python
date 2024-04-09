#!/usr/bin/python
"""Advent of Code 2019, Day 10, Part 1

https://adventofcode.com/2019/day/10

Given a map of "asteroids", figure out which asteroid has the most
asteroids in sight, without one occluding another (at same angle).

See test.dat for test data and asteroids.dat for full data.

Author: Tim Behrendsen
"""

import re
import math

fn = 'test2.dat'
fn = 'test1.dat'
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

    highest_count = 0
    for test_x, test_y in asteroids:
        # From this asteroid, compute number of unique angles

        chk = set()
        for ax, ay in asteroids:
            # Skip ourself
            if ax != test_x or ay != test_y:
                r, theta = cartesian_to_polar(ax - test_x, ay - test_y)
                chk.add(theta)

        highest_count = max(len(chk), highest_count)

    return highest_count

answer = main()
print(f"Answer is {answer}")
