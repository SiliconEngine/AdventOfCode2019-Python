#!/usr/bin/python
"""Advent of Code 2019, Day 13, Part 1 and 2

https://adventofcode.com/2019/day/13

Uses "intcode" computer from prior days. Given an intcode program that plays
breakout, figure out number of blocks to clear, then play the game and return
final score.

See program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test_prog.dat'
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

def sgn(x):
    return (x > 0) - (x < 0)

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
        self.pc = 0
        self.rel_base = 0

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

# Run program, counting how many blocks
def part1(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    tile_count = 0
    while True:
        stopped, out_list = machine.run()
        if stopped:
            break
        x = out_list[0]
        stopped, out_list = machine.run()
        y = out_list[0]
        stopped, out_list = machine.run()
        tile = out_list[0]
        if tile == 2:
            tile_count += 1

    return tile_count

tiles = { 0: ' ', 1: 'X', 2: 'B', 3:'=', 4:'O' }

def dsp_board(board):
    if not hasattr(dsp_board, 'max_x'):
        dsp_board.max_x = max([item[0] for item in board.keys()])
        dsp_board.max_y = max([item[1] for item in board.keys()])

    for y in range(0, dsp_board.max_y+1):
        print("%02d: " % (y), end='')
        for x in range(0, dsp_board.max_x+1):
            print(board.get((x, y), ' '), end='')
        print()
    print("    012345678901234567890123456789012345678901")
    return

# Run program, playing the game until no blocks left. Return score.
def part2(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    # Go through setup sequence and figure out the length, so we know
    # when game starts
    board = {}              # Visualization of the board, not actually needed
    setup_count = 0
    while True:
        stopped, out_list = machine.run()
        if stopped:
            break
        x = out_list[0]
        stopped, out_list = machine.run()
        y = out_list[0]
        stopped, out_list = machine.run()
        tile = out_list[0]
        board[(x, y)] = tiles[tile]
        setup_count += 1

    # Reset the machine, with coin inserted
    program[0] = 2
    machine.load(program)

    # Go through the setup sequence again and initialize to play
    ball_pos = (0, 0)
    paddle_pos = (0, 0)
    block_count = 0
    for i in range(setup_count):
        stopped, out_list = machine.run()
        x = out_list[0]
        stopped, out_list = machine.run()
        y = out_list[0]
        stopped, out_list = machine.run()
        t = out_list[0]
        if board[(x, y)] != tiles[t]:
            raise Exception("Setup is different")
        if t == 2:
            block_count += 1
        elif t == 4:
            ball_pos = (x, y)
        elif t == 3:
            paddle_pos = (x, y)

    # Start with no paddle move
    machine.add_input(0)
    while True:
        stopped, out_list = machine.run()
        x = out_list[0]
        stopped, out_list = machine.run()
        y = out_list[0]
        stopped, out_list = machine.run()
        t = out_list[0]

        if x >= 0:
            if t == 0 and board[(x, y)] == 'B':
                block_count -= 1

            board[(x, y)] = tiles[t]

        else:
            score = t
            if block_count == 0:
                return score

        if t == 4:
            ball_pos = (x, y)
            # when ball moves, move the paddle towards ball
            if machine.inp_len() == 0:
                move = sgn(ball_pos[0] - paddle_pos[0])
                machine.add_input(move)

        elif t == 3:
            paddle_pos = (x, y)

        if VISUALIZE:
            print("\033[H", end='')
            dsp_board(board)

    return 0

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    print(f"Part 1 answer = {part1(program)}")
    print(f"Part 2 answer = {part2(program)}")

    return

main()
