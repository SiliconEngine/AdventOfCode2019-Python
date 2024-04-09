#!/usr/bin/python
"""Advent of Code 2019, Day 20, Part 2

https://adventofcode.com/2019/day/20

Given a map with teleportation gates, calculate the shortest path. Uses Dijkstra
to calculate the path. Trickiest part was extracting the gates, which are marked
with sequences of two letters, left-to-right or north-to-south. For Part 2, the
gates transfer to a recursive "inner area", which means it needed a third
dimension coordinate for the path search.

See test0.dat,test2.dat for test data and map.dat for full data.

Author: Tim Behrendsen
"""

import re
import heapq
import sys
from collections import defaultdict 

fn = 'test0.dat'
fn = 'test2.dat'
fn = 'map.dat'

# Display the map, with optional coordinate marking
def dsp(map, c = None):
    if c != None:
        save = map[c[0]][c[1]]
        map[c[0]][c[1]] = '@'
    for line in map:
        print(''.join(line))
    if c != None:
        map[c[0]][c[1]] = save

# Diijkstra's algorithm to find path
def find_path(map, gates, gate_loc, other_gate):
    (start_row, start_col, _) = gate_loc['AA'][0]
    # Level is zero for start and end
    start_rc = (start_row, start_col)
    start_coord = (start_row, start_col, 0)
    end_rc = (gate_loc['ZZ'][0][0], gate_loc['ZZ'][0][1])
    end_coord = (gate_loc['ZZ'][0][0], gate_loc['ZZ'][0][1], 0)

    # Min/max, inclusive
    min_row, max_row = 2, len(map)-3
    min_col, max_col = 2, len(map[0])-3

    # Set up priority queue for Dijkstra
    visited = set()
    distances = { start_coord: 0 }
    unv_set = [ (0, start_row, start_col, 0) ]
    while unv_set:
        cur_node = heapq.heappop(unv_set)
        cur_row, cur_col, cur_level = cur_idx = cur_node[1:]
        cur_dist = distances[cur_idx]
        visited.add(cur_idx)

        # Stale node
        if cur_node[0] > cur_dist:
            continue

        # Found the end?
        if cur_idx == end_coord:
            return cur_dist

        # Figure out neighbor nodes
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            new_row, new_col = cur_row+dr, cur_col+dc
            if not (min_row <= new_row <= max_row and min_col <= new_col <= max_col):
                continue
            c = map[new_row][new_col]
            if c == '#' or c.isupper():
                continue
            new_dist = cur_dist + 1
            new_level = cur_level

            # Gate?
            if c != '.' and (new_row, new_col) not in (start_rc, end_rc):
                save_row, save_col, save_level = new_row, new_col, cur_level
                new_row, new_col, dir = other_gate[(new_row, new_col)]
                # Check for outer gate
                if cur_level == 0 and dir == 'I':
                    continue

                new_dist += 1
                new_level = new_level-1 if dir == 'I' else new_level+1
                if new_row == 0 or new_col == 0 or new_level < 0:
                    exit(0)

            new_idx = (new_row, new_col, new_level)

            # If node already visited, skip
            if new_idx in visited:
                continue

            new_node = (new_dist, new_row, new_col, new_level)
            new_node_dist = distances.get(new_idx, sys.maxsize)
            if new_dist < new_node_dist:
                distances[new_idx] = new_dist
                heapq.heappush(unv_set, new_node)

    raise Exception("NO PATH")

def main():
    with open(fn, 'r') as file:
        map = [ list(line.rstrip("\n")) for line in file ]

    # Build list of coordinates of letters to use to find the gates
    num_rows = len(map)
    num_cols = len(map[0])
    letter_idx = []
    for line in map:
        matches = [ (match.group(), match.start()) for match in re.finditer(r'[A-Z]', ''.join(line)) ]
        letter_idx.append(matches)

    gates = [ ]
    gate_loc = defaultdict(list)
    def add_gate(gate, row, col, dir):
        if gate not in gates: gates.append(gate)
        gate_loc[gate].append((row, col, dir))

    # Do top and bottom
    for idx, m in enumerate(letter_idx[0]):
        add_gate(m[0] + letter_idx[1][idx][0], 2, m[1], 'O')
    for idx, m in enumerate(letter_idx[num_rows-2]):
        add_gate(m[0] + letter_idx[num_rows-1][idx][0], num_rows-3, m[1], 'O')

    # Do sides
    for row, letters in enumerate(letter_idx):
        if len(letters) and letters[0][1] == 0:
            add_gate(letters[0][0] + letters[1][0], row, 2, 'O')
        if len(letters) and letters[-1][1] == (num_cols-1):
            add_gate(letters[-2][0] + letters[-1][0], row, num_cols-3, 'O')

    # Do inners
    inner_idx = 2
    while inner_idx < len(letter_idx)-2:
        inner = [ item for item in letter_idx[inner_idx] if item[1] > 1 and item[1] < num_cols-2 ]

        # Sides and top/bottom may overlap, is in the first example
        sides = [item for item in inner if not map[inner_idx+1][item[1]].isalpha()]
        tb = [item for item in inner if map[inner_idx+1][item[1]].isalpha()]

        # Side inner gate?
        if len(sides) > 1 and sides[0][1] == sides[1][1]-1:
            for idx in range(0, len(sides), 2):
                col = sides[idx][1]
                col = col-1 if col < num_cols//2 else col+2
                add_gate(sides[idx][0] + sides[idx+1][0], inner_idx, col, 'I')

        # Top/Bottom inner gate?
        if len(tb) > 0:
            for item in tb:
                row = inner_idx-1 if inner_idx < num_rows//2 else inner_idx+2
                letter2 = [ item2[0] for item2 in letter_idx[inner_idx+1] if item2[1] == item[1] ][0]
                add_gate(item[0] + letter2, row, item[1], 'I')
            inner_idx += 1      # Skip next line, already done

        inner_idx += 1

    # Build list to move to matching gate. We also mark in the map
    # each gate with a single lower-case letter to make it easier
    # to know when we hit one.
    other_gate = { }

    def flip(dir):
        return chr(ord('O')+ord('I') - ord(dir))

    for idx, (gate, locs) in enumerate(gate_loc.items()):
        for (r, c, dir) in locs:
            map[r][c] = chr(idx + ord('a'))
        if len(locs) == 1:
            other_gate[locs[0][0], locs[0][1]] = (0, 0, 'O')
        else:
            other_gate[locs[0][0], locs[0][1]] = locs[1]
            other_gate[locs[1][0], locs[1][1]] = locs[0]

    return find_path(map, gates, gate_loc, other_gate)

answer = main()
print(f"Answer is {answer}")
