#!/usr/bin/python
"""Advent of Code 2019, Day 17, Part 1 and 2

https://adventofcode.com/2019/day/17

Uses "intcode" computer from prior days. Guide a "cleaning robot" across scaffolding,
giving it a sequence of movement commands, based on a "video feed". The movement
commands must fit within a certain string length, so requires finding a specific
solution that fits the constraints.

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

# Part 1, Figure out intersections
def part1(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    # First read the image
    image = []
    line = []
    while True:
        stopped, out_list = machine.run()
        if stopped:
            break
        c = out_list[0]
        if c == 10:
            if len(line) > 0:
                image.append(''.join([ chr(c) for c in line ]))
                line = []
        else:
            line.append(c)
    if VISUALIZE:
        print("\n".join(image))

    # Scan for places where paths cross (# all around the point)
    num_rows = len(image)
    num_cols = len(image[0])
    total = 0
    for r in range(1, num_rows-1):
        for c in range(1, num_cols-1):
            if image[r+1][c] == '#' and image[r-1][c] == '#' and \
                    image[r][c+1] == '#' and image[r][c-1] == '#':

                total += r * c

    return total

# Trace the path and generate right/left turns and counts
def trace_path(image, r, c):
    num_rows = len(image)
    num_cols = len(image[0])
    dir = 'N'
    moves = { 'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1) }

    turns = { ('N', 'E'): 'R', ('N', 'W'): 'L',
        ('S', 'E'): 'L', ('S', 'W'): 'R',
        ('E', 'N'): 'L', ('E', 'S'): 'R',
        ('W', 'N'): 'R', ('W', 'S'): 'L' }

    back = { 'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E' }

    def get(r, c):
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
            return '.'
        return image[r][c]

    move_list = []
    while True:
        # Figure out what direction we're turning
        new_dir = None
        for chk_dir in ('N', 'S', 'E', 'W'):
            if chk_dir != back[dir]:
                move = moves[chk_dir]
                chk_r, chk_c = r + move[0], c + move[1]
                if get(chk_r,chk_c) == '#':
                    new_dir = chk_dir
                    break

        # End of path?
        if new_dir == None:
            break

        # Follow path until can't move further
        turn = turns[(dir, new_dir)]
        dir = new_dir
        count = 0
        while True:
            next_r, next_c = r+moves[dir][0], c + moves[dir][1]
            if get(next_r,next_c) != '#':
                break
            count += 1
            r, c = next_r, next_c

        move_list.append((turn, count))

    return move_list

# Globals for the recursive search of the patterns
g_move_list = []
g_move_list_lens = []

# Recursively check if a pattern can work
def recurse(offset, patterns, cur_list = []):
    global g_move_list

    for pattern in patterns:
        # If still room in move list for pattern
        if offset+len(pattern[1]) <= len(g_move_list):
            # Does this offset match the pattern?
            if g_move_list[offset:offset+len(pattern[1])] == pattern[1]:
                new_list = cur_list.copy()
                new_list.append(pattern[0])
                offset += len(pattern[1])
                # If reached end exactly, then we're done
                if offset == len(g_move_list):
                    return (True, new_list)

                # More to do, recurse and check more patterns
                (result, final_list) = recurse(offset, patterns, new_list)
                if result:
                    return (True, final_list)

    # No pattern matched
    return (False, [])

# Given a list of pattern segments, check if we can find a sequence that
# can deliver the moves we want, within the string length constraints.
def test_pattern(move_list, segs):
    global g_move_list, g_move_lens

    patterns = []
    letter = 'A'
    for seg in segs:
        patterns.append([ letter, g_move_list[seg[0]:seg[1]+1] ])
        letter = chr(ord(letter)+1)

    # Make sure patterns aren't repeated
    if patterns[0] == patterns[1] or patterns[0] == patterns[2] or patterns[1] == patterns[2]:
        return (False, [])

    # Check if any pattern exceeds 20 chars
    chk = []
    for p in patterns:
        total_len = 0
        for item in p[1]:
            total_len += g_move_lens[item]
        # Too long, including commas?
        if total_len + len(p[1])-1 > 20:
            return (False, [])

    # Use recursive routine to check patterns
    result, final_list = recurse(0, patterns)
    if not result:
        return (False, [])

    # Determine if final list can fit in 20 characters (letters + commas)
    if len(final_list) * 2 - 1 > 20:
        return (False, [])

    # Successful sequence found for patterns
    return result, final_list

def find_pattern(move_list):
    global g_move_list, g_move_lens

    num_moves = len(move_list)

    # Store in globals for convenience
    g_move_list = move_list
    g_move_lens = {}

    # Make an array of lengths so as to easily calculate length constraint
    for m in move_list:
        g_move_lens[m] = len(f"{m[0]},{m[1]}")

    # Do all the combinations of sequences, then test each one to see if it
    # can work. There were only 324,623 combinations, so was very tractable.
    s1_s = 0
    for s1_e in range(0, num_moves-1):
        for s2_s in range(s1_e+1, num_moves-1):
            for s2_e in range(s2_s, num_moves-1):
                for s3_s in range(s2_e+1, num_moves-1):
                    for s3_e in range(s3_s, num_moves-1):
                        (result, final_list) = test_pattern(move_list, [ (s1_s, s1_e), (s2_s, s2_e), (s3_s, s3_e) ])
                        if result:
                            segs = [ (s1_s, s1_e), (s2_s, s2_e), (s3_s, s3_e) ]

                            move_funcs = []
                            for n, s in enumerate(segs):
                                move_funcs.append(','.join([ f"{m[0]},{m[1]}" for m in move_list[s[0]:s[1]+1] ]))
                            routine = ','.join(final_list)
                            return routine, move_funcs

    raise Exception("No sequence found")

# Part 2, supply input to robot to follow the scaffolding path
def part2(program):
    machine = IntCode(yield_mode=True)
    program[0] = 2
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

    # Read video feed image from machine
    def get_image():
        # Build image
        image = []
        line = []
        robot_r, robot_c = 0, 0
        last_c = None
        while True:
            stopped, out_list = machine.run()
            c = out_list[0]
            if c == ord('^'):
                robot_r = len(image)
                robot_c = len(line)

            if c == 10:
                if len(line) > 0:
                    image.append(''.join([ chr(c) for c in line ]))
                if last_c == c:
                    break
                line = []
            else:
                line.append(c)
            last_c = c

        return image, robot_r, robot_c

    # Read initial image
    image, robot_r, robot_c = get_image()

    # Trace path of scaffolding, generating a list of turns and moves
    move_list = trace_path(image, robot_r, robot_c)

    # Figure out patterns and move routine
    routine, move_funcs = find_pattern(move_list)

    # Enter in the order to execute functions
    prompt = get_prompt()           # "Main:"
    machine.add_input_str(routine + "\n")

    # Enter in the move functions
    for f in move_funcs:
        prompt = get_prompt()       # "Function: [A,B,C]:"
        machine.add_input_str(f + "\n")

    # Either video feed or no video feed
    prompt = get_prompt()           # "Continuous video feed?"
    if not VIDEO_FEED:
        # No video feed
        machine.add_input_str('n' + "\n")

        # Outputs a final image
        image, _, _ = get_image()

    else:
        # Video feed mode
        total_moves = sum([ m[1] for m in move_list ]) + len(move_list)
        machine.add_input_str('y' + "\n")

        count = 0
        while True:
            print("\033[0;0H")
            image, _, _ = get_image()
            print('\n'.join(image))
            print()
            count += 1
            if count == total_moves:
                break

    # Get the result
    final_value = None
    while True:
        stopped, out_list = machine.run()
        if stopped:
            break
        final_value = out_list[0]

    return final_value

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    align_param = part1(program)
    print(f"Part 1: Alignment parameter = {align_param}")

    dust_count = part2(program)
    print(f"Part 2: Dust count = {dust_count}")

    return

main()
