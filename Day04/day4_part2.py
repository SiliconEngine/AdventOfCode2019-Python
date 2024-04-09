#!/usr/bin/python
"""Advent of Code 2019, Day 4, Part 2

https://adventofcode.com/2019/day/4

Compute how many passwords fit a criteria within a numeric range.

Author: Tim Behrendsen
"""

data = "153517-630395"

import re

def main():
    r1 = int(data[0:6])
    r2 = int(data[7:13])

    count = 0
    for pwd in range(r1, r2+1):
        spwd = str(pwd)

        # Have have adjacent digits and digits must increase
        # Part 2: Cannot have more than 2 adjacent in a row.
        last_d = spwd[0]
        has_adj = False
        adj_count = 1
        in_order = True
        for i in range(1, 6):
            if spwd[i] == last_d:
                adj_count += 1
            else:
                if adj_count == 2:
                    has_adj = True
                adj_count = 1

            if spwd[i] < last_d:
                in_order = False
                break
            last_d = spwd[i]

        if adj_count == 2:
            has_adj = True
        if has_adj and in_order:
            count += 1

    return count

answer = main()
print(f"Answer is {answer}")
