#!/usr/bin/python
"""Advent of Code 2019, Day 8, Part 2

https://adventofcode.com/2019/day/8

Decode an image, where each pixel is the first black/white pixel below
transparent pixels in a series of layers.

See pwd.dat for full data.

Author: Tim Behrendsen
"""

import re
import queue

fn = 'pwd.dat'

def main():
    with open(fn, 'r') as file:
        img = file.readline().rstrip("\n")

    width,height = 25, 6
    layers = []
    offset = 0
    while offset < len(img):
        offset2 = offset + width*height
        layers.append(img[offset:offset2])
        offset = offset2

    final = []
    for row in range(height):
        for col in range(width):
            offset = row * width + col
            final.append(next(lay[offset] for lay in layers if lay[offset] != '2'))

    for row in range(height):
        for col in range(width):
            offset = row * width + col
            print('X' if final[offset] == '1' else ' ', end='')
        print()

    return 

main()
