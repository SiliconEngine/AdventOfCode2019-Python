#!/usr/bin/python
"""Advent of Code 2019, Day 1, Part 2

https://adventofcode.com/2019/day/1

Sum "fuel requirements" for list of module masses using a simple formula.
Part 2 requires adding in fuel required for the mass of the fuel, in a
recursive loop (module + [weight of fuel] + [weight of that fuel] + ...)

See test.dat for sample data and mass.dat for full data.

Author: Tim Behrendsen
"""

fn = 'mass.dat'

import re

def main():
    # Read in number list
    with open(fn, 'r') as file:
        num_list = [ int(line.rstrip("\n")) for line in file ]

    total = 0
    for m in num_list:
        module_fuel = int(m/3) - 2
        fuel_n = module_fuel
        while fuel_n > 0:
            fuel_n = int(fuel_n/3) - 2
            if fuel_n < 0:
                fuel_n = 0
            module_fuel += fuel_n

        total += module_fuel

    return total

answer = main()
print(f"Answer is {answer}")
