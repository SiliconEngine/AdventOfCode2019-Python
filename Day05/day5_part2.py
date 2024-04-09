#!/usr/bin/python
"""Advent of Code 2019, Day 5, Part 2

https://adventofcode.com/2019/day/5

Interpret simple program commands, and run "diagnostics". Implements
different access modes in instruction codes, and adds new instructions.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re

POS_MODE = 0
IMM_MODE = 1
DEBUG = True

inst_list = { 1: 'SUM', 2: 'MULT', 3: 'INP', 4: 'OUT', 5: 'JT', 6: 'JF', 7: 'LT', 8: 'EQU', 99: 'END' }
lengths = { 'SUM': 3, 'MULT': 3, 'INP': 1, 'OUT': 1, 'JT': 2, 'JF': 2, 'LT': 3, 'EQU': 3, 'END': 0 }

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
        if (DEBUG):
            print(f"{pc} {inst_list[inst]}: ", end='')
            for i in range(lengths[inst_list[inst]]):
                print(f" {program[pc+i]}", end='')
            print()

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

        elif inst == 5:           # Jump-if-true
            n = get_value(modes[0], program[pc+1])
            if n != 0:
                pc = get_value(modes[1], program[pc+2])
            else:
                pc += 3

        elif inst == 6:           # Jump-if-false
            n = get_value(modes[0], program[pc+1])
            if n == 0:
                pc = get_value(modes[1], program[pc+2])
            else:
                pc += 3

        elif inst == 7:           # less-than
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            program[program[pc+3]] = 0 + (n1 < n2)
            pc += 4

        elif inst == 8:           # Equal
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            program[program[pc+3]] = 0 + (n1 == n2)
            pc += 4

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

    # Input a 5 into the program
    inp_list = [ 5 ]
    out_list = run_program(inp_list, program)

    return out_list[0]

answer = main()
print(f"Answer is {answer}")
