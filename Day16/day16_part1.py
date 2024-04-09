#!/usr/bin/python
"""Advent of Code 2019, Day 16, Part 1

https://adventofcode.com/2019/day/16

Given a list of "signal" digits, apply a transformation algorithm and repeat 100 times.
The tricky part is a pattern is applied, which itself is modified based on the position
in the digit list.

See test.dat for test data and fft.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'fft.dat'

import re
import math

def main():
    signal = []
    with open(fn, 'r') as file:
        signal = [int(c) for c in file.readline().rstrip("\n") ]
    pattern = [0, 1, 0, -1]
    pat_len = len(pattern)
    sig_len = len(signal)

    cur_list = signal.copy()
    for phase in range(100):
        new_list = []
        for i1 in range(sig_len):
            n = 0
            for i2 in range(sig_len):
                rpt_len = i1+1
                patt_idx = ((i2+1) // rpt_len) % pat_len
                n += cur_list[i2] * pattern[patt_idx]

            new_list.append(abs(n) % 10)

        cur_list = new_list.copy()

    print(''.join([ str(n) for n in cur_list[0:8] ]))

    return 0

answer = main()
print(f"Answer is {answer}")
