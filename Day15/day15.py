#!/usr/bin/python
"""Advent of Code 2019, Day 15, Part 1 and 2

https://adventofcode.com/2019/day/15

Uses "intcode" computer from prior days. An IntCode program controls a robot,
and needs to find an "oxygen system". Part 1 finds the oxygen system and
computes the number of steps. Part 2 computes the time taken for oxygen
to fill the space, which is basically the longest path.

The IntCode computer now has a save / restore state, which saved having to
implementing backtracking on the robot.

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

# Display the currently built map
def dsp(searched, wall_list, cur_x=None, cur_y=None):
    min_x, max_x, min_y, max_y = (0, 0, 0, 0)
    if len(searched) > 0:
        min_x = min([ item[0] for item in searched ])
        max_x = max([ item[0] for item in searched ])
        min_y = min([ item[1] for item in searched ])
        max_y = max([ item[1] for item in searched ])
    if cur_x != None:
        min_x = min(min_x, cur_x)
        max_x = max(max_x, cur_x)
        min_y = min(min_y, cur_y)
        max_y = max(max_y, cur_y)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) == (0, 0):
                print('S', end='')
            elif cur_x != None and (x, y) == (cur_x, cur_y):
                if (cur_x, cur_y) in wall_list:
                    print('W', end='')
                else:
                    print('O', end='')
            else:
                print(' ' if (x,y) not in wall_list else 'X', end='')
        print()

moves = [
    (0, -1),            # North
    (0, 1),             # South
    (-1, 0),            # West
    (1, 0) ]            # East

# Run program, having robot explore whole map
def part1(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    q = queue.Queue()
    wall_list = []

    # Search the map. We'll use a save/restore state on the machine, so we
    # don't have to implement backtracking, which is a hassle.
    searched = set()
    count = 0
    o2_x, o2_y, o2_path_count = 0, 0, 0
    q.put((0, 0, count, machine.save_state()))
    while not q.empty():
        x, y, count, state = q.get()
        searched.add((x, y))

        # Try each direction
        for dir in range(1, 5):
            new_x = x + moves[dir-1][0]
            new_y = y + moves[dir-1][1]
            if (new_x, new_y) in searched:
                continue

            machine.restore_state(state)
            machine.add_input(dir)
            stopped, out_list = machine.run()
            result = out_list[0]

            if result == 0:         # Wall
                wall_list.append((new_x, new_y))
                searched.add((new_x, new_y))

            elif result == 1:       # Moved OK
                q.put((new_x, new_y, count+1, machine.save_state()))

            elif result == 2:       # Found O2 system
                o2_path_count = count+1
                o2_x = new_x
                o2_y = new_y
                q.put((new_x, new_y, count+1, machine.save_state()))

    return o2_path_count, o2_x, o2_y, searched, wall_list

# Find longest path within the maze from starting point
def part2(o2_x, o2_y, wall_list):
    most_depth = 0

    q = queue.Queue()
    q.put(( o2_x, o2_y, 0))
    checked = set()
    while not q.empty():
        (x, y, count) = q.get()
        if count > most_depth:
            most_depth = count

        checked.add((x, y))
        for move in moves:
            new_x, new_y = x + move[0], y + move[1]
            if (new_x, new_y) not in wall_list and (new_x, new_y) not in checked:
                q.put((new_x, new_y, count+1))

    return most_depth

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    # Figure out entire map and location of O2 module
    o2_path_count, o2_x, o2_y, searched, wall_list = part1(program)
    if VISUALIZE:
        dsp(searched, wall_list, o2_x, o2_y)
    print(f"Part 1: distance = {o2_path_count}")

    # Find longest distance, which is the time for oxygen to spread
    mins = part2(o2_x, o2_y, wall_list)
    print(f"Part 2: mins = {mins}")

    return

main()
