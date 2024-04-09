#!/usr/bin/python
"""Advent of Code 2019, Day 12, Part 1

https://adventofcode.com/2019/day/12

Given a set of integer positions for "moons", simulate gravity according to
some simple rules. Calculate the final "energy".

See test.dat for test data and moons.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'moons.dat'

import re

def sgn(x):
    return (x > 0) - (x < 0)

def main():
    moons = []
    with open(fn, 'r') as file:
        for line in file:
            matches = re.findall('[\-0-9]+', line)
            moons.append({ 'x': int(matches[0]), 'y': int(matches[1]), 'z': int(matches[2]), 'vx': 0, 'vy': 0, 'vz': 0 })

    for step in range(1000):
        for i1 in range(4):
            for i2 in range(i1, 4):
                m1 = moons[i1]
                m2 = moons[i2]

                dx = sgn(m1['x'] - m2['x'])
                m1['vx'] -= dx;
                m2['vx'] += dx;

                dy = sgn(m1['y'] - m2['y'])
                m1['vy'] -= dy;
                m2['vy'] += dy;

                dz = sgn(m1['z'] - m2['z'])
                m1['vz'] -= dz;
                m2['vz'] += dz;

        for m in moons:
            m['x'] += m['vx']
            m['y'] += m['vy']
            m['z'] += m['vz']


    # Calculate "total energy"
    energy = 0
    for m in moons:
        pot = abs(m['x']) + abs(m['y']) + abs(m['z'])
        kin = abs(m['vx']) + abs(m['vy']) + abs(m['vz'])
        energy += pot * kin

    return energy

answer = main()
print(f"Answer is {answer}")
