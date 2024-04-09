#!/usr/bin/python
"""Advent of Code 2019, Day 16, Part 2

https://adventofcode.com/2019/day/16

Given a list of "signal" digits, repeat the digits 10,000 times and then apply
the transformation algorithm 100 times from part 1. Using the first 7 digits, use
that as the offset to return the 8 digits at that offset.

Because of the way the pattern is applied, it turns out that last 25% of the digits
follow a pattern of: digit [n] = sum(digits[n .. end]) % 10. Once that's figured
out, it's a simple matter to solve since the offset towards the end.

See test2.dat for test data and fft.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test2.dat'
fn = 'fft.dat'

import re
import math

def main():
    with open(fn, 'r') as file:
        line = file.readline().rstrip("\n")

    base_signal = [ int(c) for c in line ]
    base_sig_len = len(base_signal)

    rpt_count = 10000
    num_phases = 100
    target_offset = int(line[0:7])
    final_len = base_sig_len * rpt_count - target_offset

    # Construct array of the digits at the offset we need, to the end
    signal = []
    for i in range(final_len):
        signal.append(base_signal[(i + target_offset) % base_sig_len])

    for phase in range(num_phases):
        # Digit @[pos] = sum(digits[pos..end]) % 10
        n = 0
        for digit in range(final_len-1, -1, -1):
            n += signal[digit]
            signal[digit] = n % 10

    return ''.join([ str(d) for d in signal[0:8] ])

answer = main()
print(f"Answer is {answer}")
