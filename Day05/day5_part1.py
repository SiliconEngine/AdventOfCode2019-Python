#!/usr/bin/python
"""Advent of Code 2019, Day 5, Part 1

https://adventofcode.com/2019/day/5

Interpret simple program commands, and run "diagnostics". Implements
different access modes in instruction codes.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re

POS_MODE = 0
IMM_MODE = 1

def run_program(inp_list, program):
    pc = 0
    out_list = []
    cur_mode = POS_MODE
    mode = IMM_MODE;

    def get_value(mode, v):
        if mode == POS_MODE:            # Position mode, v = memory address
            return program[v]
        if mode == IMM_MODE:            # Immediate mode, v = actual value
            return v

    while pc < len(program):
        op = str(program[pc]).zfill(5)
        modes = [ int(op[2]), int(op[1]), int(op[0]) ]
        inst = int(op[3:])

        if inst == 1:             # sum
            n = get_value(modes[0], program[pc+1]) + get_value(modes[1], program[pc+2])
            program[program[pc+3]] = n
            pc += 4
            pass

        elif inst == 2:           # mult
            n = get_value(modes[0], program[pc+1]) * get_value(modes[1], program[pc+2])
            program[program[pc+3]] = n
            pc += 4
            pass

        elif inst == 3:           # input
            n = inp_list[0]
            program[program[pc+1]] = n
            pc += 2

        elif inst == 4:           # output
            n = get_value(modes[0], program[pc+1])
            out_list.append(n)
            pc += 2

        elif inst == 99:
            break
        
        else:
            raise Exception(f"Invalid op {inst}");

    return out_list

def main():
    program = []

    # Read in program instructions
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    # Input a 1 into the program
    inp_list = [ 1 ]
    out_list = run_program(inp_list, program)

    # Output should be all zeroes, then final number at end
    diag_code = -1
    for n in out_list[0:-1]:
        if n != 0:
            raise Exception(f"Invalid code {n}")

    return out_list[-1];

answer = main()
print(f"Answer is {answer}")
