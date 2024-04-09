#!/usr/bin/python
"""Advent of Code 2019, Day 12, Part 2

https://adventofcode.com/2019/day/12

Given a set of integer positions for "moons", simulate gravity according to
some simple rules. In part 2, we calculate how many cycles until the moons
return to their original position. Required detecting patterns in the positions
and then using a least-common-multiple.

See test.dat for test data and moons.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test2.dat'
fn = 'moons.dat'

import re
import copy
import math

def sgn(x):
    return (x > 0) - (x < 0)

def main():
    moons = []
    with open(fn, 'r') as file:
        for line in file:
            matches = re.findall('[\-0-9]+', line)
            moons.append({ 'x': int(matches[0]), 'y': int(matches[1]), 'z': int(matches[2]), 'vx': 0, 'vy': 0, 'vz': 0 })

    moons_base = copy.deepcopy(moons)

    patterns = { }
    last_step = { }
    for idx in range(4):
        for coord in ['x', 'y', 'z']:
            patterns[f"{idx}-{coord}"] = []
            last_step[f"{idx}-{coord}"] = 0

    step = 0
    have_count = 0
    last_have = 0
    while have_count < 12:
        # Simulate moon movement
        step += 1
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

        # Accumulate pattern of when we return to a position and velocity = 0
        # Stop when we've accumulate 25 samples
        have_count = 0
        for idx in range(4):
            for coord in ['x', 'y', 'z']:
                k = f"{idx}-{coord}"
                if len(patterns[k]) == 25:
                    have_count += 1
                    continue
                have_all = False

                if moons[idx][coord] == moons_base[idx][coord] and moons[idx]['v'+coord] == 0:
                    diff = step - last_step[k]
                    last_step[k] = step
                    patterns[k].append(diff)

        if have_count > last_have:
            print(have_count)
            last_have = have_count

    # Determine repeating pattern for each coordinate/velocity
    cycle_lens = []
    for idx in range(4):
        for coord in ['x', 'y', 'z']:
            k = f"{idx}-{coord}"
            pattern = patterns[k]

            # Scan pattern looking for repeat of first five
            patt_len = -1
            for i in range(1, len(pattern)+1):
                good = True
                for chk in range(0, 5):
                    if pattern[chk] != pattern[i+chk]:
                        good = False
                        break
                if good:
                    patt_len = i
                    break

            # Sum up the length of each intermediate part to get the total
            # repeating cycle
            cycle_lens.append(sum(pattern[0:patt_len]))

    # Answer is least common multiple of the pattern lengths
    return math.lcm(*cycle_lens)

answer = main()
print(f"Answer is {answer}")
