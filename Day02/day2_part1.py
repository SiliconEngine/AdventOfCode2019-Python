#!/usr/bin/python
"""Advent of Code 2019, Day 2, Part 1

https://adventofcode.com/2019/day/2

Interpret simple program commands and display result.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

#fn = 'test.dat'
fn = 'program.dat'

import re

def main():
    # Read in number list
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    program[1] = 12
    program[2] = 2

    pc = 0
    while pc < len(program):
        op = program[pc]
        if op == 1:             # sum
            n = program[program[pc+1]] + program[program[pc+2]]
            program[program[pc+3]] = n
            pc += 4
            pass

        elif op == 2:           # mult
            n = program[program[pc+1]] * program[program[pc+2]]
            program[program[pc+3]] = n
            pc += 4
            pass

        elif op == 99:
            break

    return program[0]

answer = main()
print(f"Answer is {answer}")
