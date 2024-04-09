#!/usr/bin/python
"""Advent of Code 2019, Day 1, Part 1

https://adventofcode.com/2019/day/1

Sum "fuel requirements" for list of module masses using a simple formula.

See test.dat for sample data and mass.dat for full data.

Author: Tim Behrendsen
"""

fn = 'mass.dat'

import re

def main():
    # Read in number list
    with open(fn, 'r') as file:
        num_list = [ int(line.rstrip("\n")) for line in file ]

    answer = sum([ int(m/3) - 2 for m in num_list ]);
    return answer

answer = main()
print(f"Answer is {answer}")
