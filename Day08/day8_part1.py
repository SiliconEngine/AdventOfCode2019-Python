#!/usr/bin/python
"""Advent of Code 2019, Day 8, Part 1

https://adventofcode.com/2019/day/8

Decode an image that consists of a series of layers. Find the one
with the fewest '0' pixels, and the multiply the number of '1' and '2'
pixels.

See pwd.dat for full data.

Author: Tim Behrendsen
"""

import re
import queue

fn = 'pwd.dat'

def main():
    with open(fn, 'r') as file:
        img = file.readline().rstrip("\n")

    #print(img)
    width = 25
    height = 6

    layers = []
    offset = 0
    while offset < len(img):
        offset2 = offset + width*height
        layers.append(img[offset:offset2])
        offset = offset2

    print(f"{len(layers)} Layers")

    layer_totals = []
    for lay in layers:
        totals = { 0: 0, 1: 0, 2: 0 }
        for c in lay:
            totals[int(c)] += 1
        layer_totals.append(totals)

    print(layer_totals)
    layer_totals.sort(key=lambda item: item[0])
    print(layer_totals)

    return layer_totals[0][1] * layer_totals[0][2]

answer = main()
print(f"Answer is {answer}")
