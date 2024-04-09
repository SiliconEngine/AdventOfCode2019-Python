#!/usr/bin/python
"""Advent of Code 2019, Day 18, Part 1

https://adventofcode.com/2019/day/18

Given a map with doors and keys that must be visited, find the shortest path
to gather the keys and unlock the doors. Uses Dijkstra with coordinates and
the set of gathered keys.

See test1.dat-test4.dat for test data and map.dat for full data.

Author: Tim Behrendsen
"""

import re
import heapq
import sys

fn = 'test1.dat'
fn = 'test2.dat'
fn = 'test3.dat'
fn = 'test4.dat'
fn = 'map.dat'

# Return character at map, accounting for doors opened/closed
def get_map(map, keys, row, col):
    c = map[row][col]

    # If a door or a key and unlocked, then set as empty
    if c.isalpha() and ((1 << (ord(c.lower())-ord('a'))) & keys) != 0:
        return '.'

    # If a door still locked, then treat as a wall
    if c.isupper():
        return '#'

    return c

def calc_paths(map, key_list, start_row, start_col):
    # Key list will be a bitmap
    end_key_set = 2**len(key_list) - 1

    # Set up priority queue for Dijkstra
    visited = set()
    unv_set = [ (0, start_row, start_col, 0) ]
    distances = { (start_row, start_col, 0): 0 }

    while unv_set:
        cur_node = heapq.heappop(unv_set)
        cur_row, cur_col, cur_keys = cur_node[1:4]
        cur_idx = cur_node[1:]
        cur_dist = distances[cur_idx]
        visited.add(cur_idx)
        new_dist = cur_dist + 1

        # Stale node
        if cur_node[0] > cur_dist:
            continue

        # Found all the keys?
        if cur_keys == end_key_set:
            return cur_dist

        # Figure out neighbor nodes
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            new_row, new_col = cur_row+dr, cur_col+dc
            c = get_map(map, cur_keys, new_row, new_col)
            if c == '#':
                continue

            # If a new key, then add to unlocked key list and gen new node
            new_keys = cur_keys
            if c.islower():
                new_keys = cur_keys | (1 << ord(c) - ord('a'))

            new_idx = (new_row, new_col, new_keys)

            # If node already visited, skip
            if new_idx in visited:
                continue

            new_node = (new_dist, new_row, new_col, new_keys)
            new_node_dist = distances.get(new_idx, sys.maxsize)
            if new_dist < new_node_dist:
                distances[new_idx] = new_dist
                heapq.heappush(unv_set, new_node)

def main():
    with open(fn, 'r') as file:
        map = [ line.rstrip("\n") for line in file ]
    start_row, start_col = [ (r, line.find('@')) for r, line in enumerate(map) if line.find('@') >= 0 ][0]
    key_list = [ c for line in map for c in line if c.islower() ]

    return calc_paths(map, key_list, start_row, start_col)

answer = main()
print(f"Answer is {answer}")
