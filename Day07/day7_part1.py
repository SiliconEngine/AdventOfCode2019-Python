#!/usr/bin/python
"""Advent of Code 2019, Day 7, Part 1

https://adventofcode.com/2019/day/7

Uses "intcode" computer from prior days. Find the highest "thrust"
value by finding the optimal combination of input values that produces
the highest number.

See test.dat for sample data and program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re

POS_MODE = 0
IMM_MODE = 1
DEBUG = False

inst_list = { 1: 'SUM', 2: 'MULT', 3: 'INP', 4: 'OUT', 5: 'JT', 6: 'JF', 7: 'LT', 8: 'EQU', 99: 'END' }
lengths = { 'SUM': 3, 'MULT': 3, 'INP': 1, 'OUT': 1, 'JT': 2, 'JF': 2, 'LT': 3, 'EQU': 3, 'END': 0 }

def run_program(inp_list, program):
    pc = 0
    out_list = []
    cur_mode = POS_MODE
    mode = IMM_MODE;
    inp_idx = 0

    def get_value(mode, v):
        if mode == POS_MODE:            # Position mode, v = memory address
            return program[v]
        if mode == IMM_MODE:            # Immediate mode, v = actual value
            return v

    while pc < len(program):
        op = program[pc];
        modes = [ (op // 100) % 10, (op // 1000) % 10, op // 10000 ]
        inst = op % 100;

        if (DEBUG):
            print(f"{pc} {inst_list[inst]}: ", end='')
            for i in range(lengths[inst_list[inst]]):
                print(f" {program[pc+i]}", end='')
            print()

        if inst == 1:             # sum
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            n = n1 + n2
            program[program[pc+3]] = n
            if (DEBUG):
                print(f"    SUM: {n1} + {n2} = {n}, store at {program[pc+3]}")
            pc += 4
            pass

        elif inst == 2:           # mult
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            n = n1 * n2
            program[program[pc+3]] = n
            if (DEBUG):
                print(f"    MULT: {n1} * {n2} = {n}, store at {program[pc+3]}")
            pc += 4
            pass

        elif inst == 3:           # input
            n = inp_list[inp_idx]
            inp_idx += 1
            program[program[pc+1]] = n
            if (DEBUG):
                print(f"    INP: {n} store at {program[pc+1]}")
            pc += 2

        elif inst == 4:           # output
            n = get_value(modes[0], program[pc+1])
            out_list.append(n)
            if (DEBUG):
                print(f"    OUT: {n} write from {program[pc+1]}")
            pc += 2

        elif inst == 5:           # Jump-if-true
            n = get_value(modes[0], program[pc+1])
            if n != 0:
                pc = get_value(modes[1], program[pc+2])
                if (DEBUG):
                    print(f"    JT: {n}, jumping to {program[pc+2]}")
            else:
                print(f"    JT: {n}, NO JUMP")
                pc += 3

        elif inst == 6:           # Jump-if-false
            n = get_value(modes[0], program[pc+1])
            if n == 0:
                pc = get_value(modes[1], program[pc+2])
                if (DEBUG):
                    print(f"    JF: {n}, jumping to {program[pc+2]}")
            else:
                print(f"    JF: {n}, NO JUMP")
                pc += 3

        elif inst == 7:           # less-than
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            program[program[pc+3]] = 0 + (n1 < n2)
            if (DEBUG):
                print(f"    LT: {n1} < {n2} = {n1 < n2}, store at {program[pc+3]}")
            pc += 4

        elif inst == 8:           # Equal
            n1 = get_value(modes[0], program[pc+1])
            n2 = get_value(modes[1], program[pc+2])
            program[program[pc+3]] = 0 + (n1 == n2)
            if (DEBUG):
                print(f"    EQ: {n1} = {n2} = {n1 == n2}, store at {program[pc+3]}")
            pc += 4

        elif inst == 99:
            break
        
        else:
            raise Exception(f"Invalid op {inst}");

    return out_list

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    # Calculate signal based on sequence
    def calc_signal(seq):
        n = 0
        for s in seq:
            rp = program.copy()
            out_list = run_program([ s, n ], rp)
            n = out_list[0]
        return n

    # Search all sequences and figure out largest
    max_num = 0
    for s1 in range(5):
        for s2 in range(5):
            if s2 == s1:
                continue
            for s3 in range(5):
                if s3 in (s1, s2):
                    continue
                for s4 in range(5):
                    if s4 in (s1, s2, s3):
                        continue
                    for s5 in range(5):
                        if s5 in (s1, s2, s3, s4):
                            continue
                        n = calc_signal([s1, s2, s3, s4, s5])
                        max_num = max(max_num, n)

    return max_num

answer = main()
print(f"Answer is {answer}")
