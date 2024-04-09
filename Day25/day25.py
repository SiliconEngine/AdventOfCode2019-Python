#!/usr/bin/python
"""Advent of Code 2019, Day 25

https://adventofcode.com/2019/day/25

Uses "intcode" computer from prior days. Plays an interactive "adventure" game
and has to find a combination of picked-up items that allows moving past a
security checkpoint. It automatically navigates the map, accumulates the items
and tries combinations of items until it gets past the security checkpoint.

See program.dat for full data.

Author: Tim Behrendsen
"""

fn = 'program.dat'

import re
import queue

INTERACTIVE = False
VISUALIZE = True
DEBUG = False

POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2

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

# Read back output from IntCode
def get_prompt(machine, die = True):
    char_list = []
    lines = []
    while True:
        stopped, out_list = machine.run()
        if stopped:
            if die:
                print("ROBOT DIED")
                exit(0)
            return stopped, lines

        c = out_list[0]
        if c == 10:
            line = ''.join(char_list)
            if VISUALIZE:
                print(line)
            lines.append(line)
            if stopped or line == "Command?":
                return stopped, lines
            char_list = []
            continue

        char_list.append(chr(c))


back_list = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
}

# Items that trigger traps
bad_items = [
    'molten lava',
    'photons',
    'giant electromagnet',
    'infinite loop',
    'escape pod',
]

item_list = set()

room_paths = { }

def explore(machine, came_from=None, path=[]):
    stopped, prompt = get_prompt(machine)

    # Get name of room and store current path
    line = next(( line for line in prompt if line.startswith('== ')), -1)
    name = re.findall(r'== (.*) ==', line)[0]
    room_paths[name] = path

    # Find valid directions
    dirs = []
    idx = [ idx for idx, line in enumerate(prompt) if 'lead' in line ][0]
    while prompt[idx := idx+1].startswith('- '):
        dirs.append(prompt[idx][2:])

    # See what can be picked up
    items = []
    idx = next(( idx for idx, line in enumerate(prompt) if 'here:' in line ), -1)
    while prompt[idx := idx+1].startswith('- '):
        items.append(prompt[idx][2:])

    # Pick up the items, if it's not on the bad list
    for item in items:
        if item in bad_items:
            continue
        machine.add_input_str(f"take {item}\n")
        item_list.add(item)
        stopped, prompt = get_prompt(machine)

    # Recursively navigate each direction
    for dir in dirs:
        if back_list[dir] == came_from:
            continue
        if VISUALIZE:
            print(f"MOVING TO: {dir}")

        # Move to new room
        new_path = path.copy()
        new_path.append(dir)
        machine.add_input_str(f"{dir}\n")
        explore(machine, dir, new_path)

        # Move back
        if VISUALIZE:
            print(f"MOVING BACK TO: {back_list[dir]}")
        machine.add_input_str(f"{back_list[dir]}\n")
        stopped, prompt = get_prompt(machine)

    return

# Interactive mode
def interactive(machine):
    save_slots = { }
    stopped, prompt = get_prompt(machine, False)

    while True:
        cmd = input("> ")
        if cmd.startswith('save '):
            save_slots[cmd[5:]] = machine.save_state()
            print("SAVED")
            continue
        elif cmd.startswith('rest '):
            if save_slots.get(cmd[5:]) == None:
                print("BAD SLOT")
            else:
                machine.restore_state(save_slots[cmd[5:]])
                print("RESTORED")
            continue

        machine.add_input_str(cmd + "\n")
        stopped, prompt = get_prompt(machine, False)
        if stopped:
            print("ROBOT DIED, restarting")
            machine.reset()
            stopped, prompt = get_prompt(machine, False)

    return 0

# Adventure
def adventure(program):
    machine = IntCode(yield_mode=True)
    machine.load(program)

    if INTERACTIVE:
        global VISUALIZE
        VISUALIZE = True
        interactive(machine)

    # Explore map and gather items
    explore(machine)
    items = list(item_list)

    # Display inventory we gathered
    if VISUALIZE:
        machine.add_input_str("inv\n")
        get_prompt(machine)

    # Navigate to security checkpoint
    for dir in room_paths['Security Checkpoint']:
        machine.add_input_str(f"{dir}\n")
        get_prompt(machine)

    # Drop all our items here
    for item in items:
        machine.add_input_str(f"drop {item}\n")
        stopped, prompt = get_prompt(machine)

    # Try each combination of items until it works
    for combo in range(1, 256):
        # Combo is bitmap of what items to try
        try_items = []
        for idx in range(len(items)):
            if combo & (2 ** idx):
                try_items.append(items[idx])

        # Pick up items we're going to try
        if VISUALIZE:
            print(f"TRYING: {try_items}")
        for item in try_items:
            cmd = f"take {item}\n"
            if VISUALIZE:
                print(f"SENDING: {cmd}")
            machine.add_input_str(cmd)
            stopped, prompt = get_prompt(machine)

        # Test the combo and see if we get through
        machine.add_input_str(f"west\n")
        stopped, prompt = get_prompt(machine, False)
        if stopped:
            num = re.findall('\d+', prompt[-1])[0]
            return num

        # Drop the items we just tried
        for item in try_items:
            cmd = f"drop {item}\n"
            if VISUALIZE:
                print(f"SENDING: {cmd}")
            machine.add_input_str(cmd)
            stopped, prompt = get_prompt(machine)

    print("Could not get through")
    exit(0)

def main():
    # Read in program instructions
    program = []
    with open(fn, 'r') as file:
        program = [ int(n) for n in file.readline().rstrip("\n").split(',') ]

    answer = adventure(program)
    print(f"Lock code = {answer}")

    return

main()
