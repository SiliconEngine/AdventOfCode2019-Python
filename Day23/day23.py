#!/usr/bin/python
"""Advent of Code 2019, Day 23, Part 1 and 2

https://adventofcode.com/2019/day/23


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
    # no_inp_block:
    #       False = Stop if no input
    #       True  = Return -1 in input instruction, if no input
    def __init__(self, yield_mode = False, no_inp_block = False):
        self.memory = { }
        self.rel_base = 0
        self.yield_mode = yield_mode
        self.input_queue = queue.Queue()
        self.no_inp_block = no_inp_block

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

    def get_input(self):
        if DEBUG:
            print(f"    get_input: len = {self.inp_len()}")
        if self.no_inp_block and self.inp_len() == 0:
            return -1
        return self.input_queue.get()

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
                # If no block mode and no current input, store -1 and yield
                if self.no_inp_block and self.inp_len() == 0:
                    addr = self.store_val(modes[0], params[0], -1)
                    self.pc += 2
                    return 0, out_list

                n = self.get_input()
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

def allocate_network(program):
    # Allocate 50 machines
    network = []
    for addr in range(50):
        machine = IntCode(yield_mode=True, no_inp_block=True)
        machine.load(program)
        network.append(machine)

        # First input is "network address"
        machine.add_input(addr)
        stopped, out_list = machine.run()

    return network

# Part 1
def part1(program):
    network = allocate_network(program)

    # Continue until something sent to address "255"
    while True:
        for addr in range(50):
            machine = network[addr]
            stopped, out_list = machine.run()

            # See if machine output a message to send to another machine
            if len(out_list) > 0:
                dest_addr = out_list[0]             # Address
                stopped, out_list = machine.run()
                x = out_list[0]                     # X parameter
                stopped, out_list = machine.run()
                y = out_list[0]                     # Y parameter
                if dest_addr == 255:
                    return y
                # Send to destination
                network[dest_addr].add_input(x)
                network[dest_addr].add_input(y)

    return 0

# Part 2
def part2(program):
    network = allocate_network(program)

    last_y = -99
    nat = (-1, -1)

    # Continue until same "Y" sent to 255 twice
    while True:
        idle = True
        for addr in range(50):
            machine = network[addr]
            stopped, out_list = machine.run()
            if len(out_list) > 0:
                dest_addr = out_list[0]
                stopped, out_list = machine.run()
                x = out_list[0]
                stopped, out_list = machine.run()
                y = out_list[0]

                # Write to NAT
                if dest_addr == 255:
                    nat = (x, y)
                else:
                    network[dest_addr].add_input(x)
                    network[dest_addr].add_input(y)
                    idle = False

        if idle:
            if nat[1] == last_y:
                return last_y
            network[0].add_input(nat[0])
            network[0].add_input(nat[1])
            last_y = nat[1]

    return 0

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
