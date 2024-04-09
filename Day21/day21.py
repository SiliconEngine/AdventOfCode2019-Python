#!/usr/bin/python
"""Advent of Code 2019, Day 21, Part 1 and 2

https://adventofcode.com/2019/day/21

Uses "intcode" computer from prior days. Given a jumping robot equipped with hole
sensors, we must give it a sequence of boolean instructions to navigate over a 1D
terrain. Required getting a little further and analyzing what rules would jump over
the holes of different sizes.

See program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re
import queue

POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2
DEBUG = False
VISUALIZE = False
VIDEO_FEED = False

inst_list = { 1: 'SUM', 2: 'MULT', 3: 'INP', 4: 'OUT', 5: 'JT', 6: 'JF', 7: 'LT', 8: 'EQU', 9: 'REL', 99: 'END' }
lengths = { 'SUM': 3, 'MULT': 3, 'INP': 1, 'OUT': 1, 'JT': 2, 'JF': 2, 'LT': 3, 'EQU': 3, 'REL': 1, 'END': 0 }

class IntCode:
    # yield_mode:
    #       False = Run until END opcode
    #       True  = Return result when output written to, continue when called again
    def __init__(self, yield_mode = False):
        self.memory = { }
        self.rel_base = 0
        self.yield_mode = yield_mode
        self.input_queue = queue.Queue()

    # Load program into memory and reset computer
    def load(self, program):
        self.memory = { int(i): int(value) for i, value in enumerate(program) }
        self.base_memory = self.memory.copy()
        self.pc = 0
        self.rel_base = 0

    # Reset the program to base state
    def reset(self):
        self.pc = 0
        self.rel_base = 0
        for i, val in self.base_memory.items():
            self.memory[i] = val

    # Save state of program
    def save_state(self):
        # Return list of differences from current state to saved state
        diff = [ (i, val) for i, val in self.memory.items() \
            if i not in self.base_memory or self.base_memory.get(i, 0) != val ]

        return [ self.rel_base, self.pc, diff ]

    def restore_state(self, state):
        self.rel_base = state[0]
        self.pc = state[1]
        for i, val in self.base_memory.items():
            self.memory[i] = val

        for diff in state[2]:
            self.memory[diff[0]] = diff[1]
        return

    # Fetch a memory location
    def fetch(self, addr):
        if DEBUG:
            print(f"    Fetch [{addr}] is {self.memory.get(addr, 0)}")
        if addr < 0:
            raise Exception("Invalid fetch: {addr}")
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

    def add_input(self, n):
        self.input_queue.put(n)

    def add_input_str(self, s):
        for c in s:
            self.input_queue.put(ord(c))

    def inp_len(self):
        return self.input_queue.qsize()

    # Run program
    def run(self):
        out_list = []

        while True:
            op = self.memory.get(self.pc)
            inst = op % 100;
            modes = [ (op // 100) % 10, (op // 1000) % 10, op // 10000 ]
            params = [ self.memory.get(self.pc+i+1, 0) for i in range(lengths[inst_list[inst]]) ]

            if DEBUG:
                print(f"{self.pc} {inst_list[inst]} ({op} / {modes}): {params}")

            if inst == 1:             # sum
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                n = n1 + n2
                addr = self.store_val(modes[2], params[2], n)
                if DEBUG:
                    print(f"    SUM: {n1} + {n2} = {n}, store at [{addr}]")
                self.pc += 4
                pass

            elif inst == 2:           # mult
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                n = n1 * n2
                addr = self.store_val(modes[2], params[2], n)
                if DEBUG:
                    print(f"    MULT: {n1} * {n2} = {n}, store at [{addr}]")
                self.pc += 4
                pass

            elif inst == 3:           # input
                n = self.input_queue.get()
                addr = self.store_val(modes[0], params[0], n)
                if DEBUG:
                    print(f"    INP: {n} store at [{addr}]")
                self.pc += 2

            elif inst == 4:           # output
                n = self.fetch_val(modes[0], params[0])
                out_list.append(n)
                if DEBUG:
                    print(f"    OUT: {n} write from {params[0]}")
                self.pc += 2
                if self.yield_mode:
                    return 0, out_list

            elif inst == 5:           # Jump-if-true
                n = self.fetch_val(modes[0], params[0])
                if n != 0:
                    self.pc = self.fetch_val(modes[1], params[1])
                    if DEBUG:
                        print(f"    JT: {n}, jumping to {self.pc}")
                else:
                    if DEBUG:
                        print(f"    JT: {n}, NO JUMP")
                    self.pc += 3

            elif inst == 6:           # Jump-if-false
                n = self.fetch_val(modes[0], params[0])
                if n == 0:
                    self.pc = self.fetch_val(modes[1], params[1])
                    if DEBUG:
                        print(f"    JF: {n}, jumping to {self.pc}")
                else:
                    if DEBUG:
                        print(f"    JF: {n}, NO JUMP")
                    self.pc += 3

            elif inst == 7:           # less-than
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                addr = self.store_val(modes[2], params[2], 0 + (n1 < n2))
                if DEBUG:
                    print(f"    LT: {n1} < {n2} = {n1 < n2}, store at [{addr}]")
                self.pc += 4

            elif inst == 8:           # Equal
                n1 = self.fetch_val(modes[0], params[0])
                n2 = self.fetch_val(modes[1], params[1])
                addr = self.store_val(modes[2], params[2], 0 + (n1 == n2))
                if DEBUG:
                    print(f"    EQ: {n1} == {n2}, is {n1 == n2}, store at [{addr}]")
                self.pc += 4

            elif inst == 9:           # Set relative base
                last = self.rel_base
                self.rel_base += self.fetch_val(modes[0], params[0])
                if DEBUG:
                    print(f"    REL: Relative base set from {last} to {self.rel_base}")
                self.pc += 2

            elif inst == 99:
                break
            
            else:
                raise Exception(f"Invalid op {inst}");

        return 1, out_list

# After sending instruction, gather the success value to display
def get_success_value(machine):
    success_value = -1
    while True:
        stopped, out_list = machine.run()
        if stopped:
            break
        if out_list[0] > 255:
            success_value = out_list[0]
            break

        #print(chr(out_list[0]), end='')

    return success_value

# Part 1, jump over holes using "springscript" in "WALK" mode
def part1(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    # Read prompt from machine
    def get_prompt():
        char_list = []
        while True:
            stopped, out_list = machine.run()
            c = out_list[0]
            if c == 10:
                return ''.join(char_list)
            char_list.append(chr(c))

    # Enter in the order to execute functions
    prompt = get_prompt()
    machine.add_input_str("OR A J\n")       # J = A-ground
    machine.add_input_str("NOT C T\n")      # T = C-hole
    machine.add_input_str("AND T J\n")      # J = A-ground & C-hole
    machine.add_input_str("AND D J\n")      # J = A-ground & C-hole & D-ground
    machine.add_input_str("NOT A T\n")      # T = A-hole
    machine.add_input_str("OR T J\n")       # T = A-hole | (a-ground & c-hole & d-ground)
    machine.add_input_str("WALK\n")

    return get_success_value(machine)

# Part 2, jump over holes using "springscript" in "RUN" mode
def part2(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    # Read prompt from machine
    def get_prompt():
        char_list = []
        while True:
            stopped, out_list = machine.run()
            c = out_list[0]
            if c == 10:
                return ''.join(char_list)
            char_list.append(chr(c))

    prompt = get_prompt()

    machine.add_input_str("NOT B J\n")          # J = B-hole
    machine.add_input_str("NOT C T\n")          # T = C-hole
    machine.add_input_str("OR T J\n")           # J = (B-hole | C-hole)
    machine.add_input_str("AND D J\n")          # J = D-ground & (B-hole | C-hole)
    machine.add_input_str("AND H J\n")          # J = H-ground & D-ground & (B-hole | C-hole)
    machine.add_input_str("NOT A T\n")          # T = A-hole
    machine.add_input_str("OR T J\n")           # J = A-Hole | (H-ground & D-ground & (B-hole | C-hole))
    machine.add_input_str("RUN\n")

    return get_success_value(machine)

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    answer = part1(program)
    print(f"Part 1: answer = {answer}")

    answer = part2(program)
    print(f"Part 2: answer = {answer}")

    return

main()
