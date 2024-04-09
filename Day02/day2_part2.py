#!/usr/bin/python
"""Advent of Code 2019, Day 2, Part 2

https://adventofcode.com/2019/day/2

Interpret simple program commands, and search for combination of
parameters that return 19690720.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re

def run_program(program):
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

def main():
    program = []

    # Read in number list
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    for i in range(100):
        for j in range(100):
            copy_program = program.copy()
            copy_program[1] = i
            copy_program[2] = j
            result = run_program(copy_program)
            if result == 19690720:
                return i * 100 + j;

answer = main()
print(f"Answer is {answer}")
