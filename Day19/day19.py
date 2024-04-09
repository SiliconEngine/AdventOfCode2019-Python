#!/usr/bin/python
"""Advent of Code 2019, Day 19, Part 1 and 2

https://adventofcode.com/2019/day/19

Uses "intcode" computer from prior days. Program is a "drone" that can return
whether a particular point is within a "tractor beam". Part 1 is counting
the number of beam squares within a 50x50 grid. Part 2 is figuring out the
closest point where a 100x100 square fill fit within the beam.

See program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re
import queue
import math

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

# Part 1, count the number of beam squares
def part1(program):
    machine = IntCode(yield_mode=False)
    machine.load(program)

    # Build the image and count the squares. Image not actually needed.
    image = []
    count = 0
    for y in range(50):
        line = []
        for x in range(50):
            machine.reset()
            machine.add_input(x)
            machine.add_input(y)
            stopped, out_list = machine.run()
            line.append('#' if out_list[0] != 0 else '.')
            count += out_list[0]
        image.append(''.join(line))

    return count

# Check if the 100x100 square will fit at x,y
def check_fit(ranges, x, y):
    box_x, box_y = 100, 100
    # Check x
    if x < 0:
        return False
    r = ranges[y]
    if not (x >= r[0] and (x+box_x-1) <= r[1]):
        return False
    # Check y
    r = ranges[y+box_y-1]
    return x >= r[0] and x <= r[1]

# Part 1, figure out the closest a 100x100 square will fit in the beam
def part2(program):
    machine = IntCode(yield_mode=False)
    machine.load(program)

    def get(x, y):
        if x < 0:
            raise Exception(f"x is {x}")

        machine.reset()
        machine.add_input(x)
        machine.add_input(y)
        stopped, out_list = machine.run()
        return out_list[0]

    # Scan each line, figuring out the range of the beam
    # To check our 100x100 square, we'll need the ranges to be
    # at least that far ahead
    scan_y = 20
    cur_x = 0
    cur_width = 0
    best_dist = 9999999
    best_coord = None
    ranges = {}
    while True:
        scan_y += 1

        # Scan forward for edge of beam
        x1 = cur_x-1
        while True:
            x1 += 1
            if get(x1, scan_y):
                break

        # Scan backward for edge of beam
        x2 = x1+cur_width+5
        while True:
            x2 -= 1
            if get(x2, scan_y):
                break

        cur_x = x1
        cur_width = x2-x1-1
        ranges[scan_y] = (x1, x2)

        if scan_y > 200:
            y = scan_y - 150
            if best_coord != None:
                # Continue on for another 100 after the best, just in case
                if y - best_coord[1] > 100:
                    break

            r = ranges[y]
            mid_x = (r[0] + r[1]) // 2
            for x in range(mid_x - 50, mid_x + 50):
                if check_fit(ranges, x, y):
                    dist = math.sqrt(x**2 + y**2)
                    if dist < best_dist:
                        best_coord = (x, y)
                        best_dist = dist

    return best_coord[0] * 10000 + best_coord[1]

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
