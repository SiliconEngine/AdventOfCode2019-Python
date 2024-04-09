#!/usr/bin/python
"""Advent of Code 2019, Day 9, Part 1 and Part 2

https://adventofcode.com/2019/day/9

Uses "intcode" computer from prior days. Adds a new "relative mode" for addressing.

See program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re

POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2
DEBUG = False

inst_list = { 1: 'SUM', 2: 'MULT', 3: 'INP', 4: 'OUT', 5: 'JT', 6: 'JF', 7: 'LT', 8: 'EQU', 9: 'REL', 99: 'END' }
lengths = { 'SUM': 3, 'MULT': 3, 'INP': 1, 'OUT': 1, 'JT': 2, 'JF': 2, 'LT': 3, 'EQU': 3, 'REL': 1, 'END': 0 }

class IntCode:
    def __init__(self):
        self.memory = { }
        self.rel_base = 0

    # Load program into memory
    def load(self, program):
        self.memory = { int(i): int(value) for i, value in enumerate(program) }

    # Fetch a memory location
    def fetch(self, addr):
        if DEBUG:
            print(f"    Fetch [{addr}] is {self.memory.get(addr, 0)}")
        return self.memory.get(addr, 0)

    # Fetch a memory location with mode
    def fetch_val(self, mode, val):
        if mode == POS_MODE:            # Position mode, val = memory address
            return self.fetch(val)
        if mode == IMM_MODE:            # Immediate mode, val = actual value
            return val
        if mode == REL_MODE:            # Relative mode, val = offset from relative base
            return self.fetch(val+self.rel_base)
        raise Exception("invalid mode {mode}")

    # Store at memory location
    def store(self, addr, val):
        self.memory[addr] = val
        if DEBUG:
            print(f"    Write to [{addr}] <- {val}")

    # Store at memory location with mode
    def store_val(self, mode, addr, val):
        if mode == POS_MODE:            # Position mode, val = memory address
            pass
        elif mode == REL_MODE:          # Relative mode, val = offset from relative base
            addr = addr + self.rel_base
        else:
            raise Exception("invalid mode {mode}")

        self.store(addr, val)
        return addr

    # Run program
    def run(self, inp_list):
        pc = 0
        out_list = []
        inp_idx = 0
        self.rel_base = 0

        while True:
            op = self.memory.get(pc)
            inst = op % 100;
            modes = [ (op // 100) % 10, (op // 1000) % 10, op // 10000 ]
            params = [ self.memory.get(pc+i+1, 0) for i in range(lengths[inst_list[inst]]) ]

            if DEBUG:
                print(f"{pc} {inst_list[inst]} ({op} / {modes}): {params}")

            if inst == 1:             # sum
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                n = n1 + n2
                addr = self.store_val(modes[2], params[2], n)
                if DEBUG:
                    print(f"    SUM: {n1} + {n2} = {n}, store at [{addr}]")
                pc += 4
                pass

            elif inst == 2:           # mult
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                n = n1 * n2
                addr = self.store_val(modes[2], params[2], n)
                if DEBUG:
                    print(f"    MULT: {n1} * {n2} = {n}, store at [{addr}]")
                pc += 4
                pass

            elif inst == 3:           # input
                n = inp_list[inp_idx]
                inp_idx += 1
                addr = self.store_val(modes[0], params[0], n)
                if DEBUG:
                    print(f"    INP: {n} store at [{addr}]")
                pc += 2

            elif inst == 4:           # output
                n = self.fetch_val(modes[0], params[0])
                out_list.append(n)
                if DEBUG:
                    print(f"    OUT: {n} write from {params[0]}")
                pc += 2

            elif inst == 5:           # Jump-if-true
                n = self.fetch_val(modes[0], params[0])
                if n != 0:
                    pc = self.fetch_val(modes[1], params[1])
                    if DEBUG:
                        print(f"    JT: {n}, jumping to {pc}")
                else:
                    if DEBUG:
                        print(f"    JT: {n}, NO JUMP")
                    pc += 3

            elif inst == 6:           # Jump-if-false
                n = self.fetch_val(modes[0], params[0])
                if n == 0:
                    pc = self.fetch_val(modes[1], params[1])
                    if DEBUG:
                        print(f"    JF: {n}, jumping to {pc}")
                else:
                    if DEBUG:
                        print(f"    JF: {n}, NO JUMP")
                    pc += 3

            elif inst == 7:           # less-than
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                addr = self.store_val(modes[2], params[2], 0 + (n1 < n2))
                if DEBUG:
                    print(f"    LT: {n1} < {n2} = {n1 < n2}, store at [{addr}]")
                pc += 4

            elif inst == 8:           # Equal
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                addr = self.store_val(modes[2], params[2], 0 + (n1 == n2))
                if DEBUG:
                    print(f"    EQ: {n1} == {n2}, is {n1 == n2}, store at [{addr}]")
                pc += 4

            elif inst == 9:           # Set relative base
                self.rel_base += self.fetch_val(modes[0], params[0])
                if DEBUG:
                    print(f"    REL: Relative base set to {self.rel_base}")
                pc += 2

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

    machine = IntCode()
    machine.load(program)
    out_list = machine.run([ 1 ])
    print(f"Part 1 is {out_list[0]}")

    machine.load(program)
    out_list = machine.run([ 2 ])
    print(f"Part 2 is {out_list[0]}")

    return

main()
