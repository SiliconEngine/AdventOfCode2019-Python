#!/usr/bin/python
"""Advent of Code 2019, Day 18, Part 2

https://adventofcode.com/2019/day/18

Given a map with doors and keys that must be visited, find the shortest path
to gather the keys and unlock the doors. In part 2, we have for robots that
traverse isolated quadrants of the map. Uses two Dijkstra searches, an
inner one that figures out what keys are traversable, and then an outer main
Dijkstra that uses the key coordinates + current keys gathered.

See test5.dat-test8.dat for test data and map.dat for full data.

Author: Tim Behrendsen
"""

import heapq
import sys

fn = 'test5.dat'
fn = 'test6.dat'
fn = 'test7.dat'
fn = 'test8.dat'
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

# Find all keys currently accessible using Dijkstra's algorithm
def find_keys(map, keys, start_row, start_col):
    visited = set()
    distances = { (start_row, start_col): 0 }
    unv_set = [ (0, start_row, start_col) ]
    move_list = []

    while unv_set:
        node = heapq.heappop(unv_set)
        node_dist, row, col = node
        cur_dist = distances[(row, col)]

        # Stale node
        if node_dist > cur_dist:
            continue

        visited.add((row, col))
        new_dist = cur_dist + 1

        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            new_row, new_col = row+dr, col+dc
            if (new_row, new_col) in visited:
                continue

            c = get_map(map, keys, new_row, new_col)
            if c == '#':
                continue

            # Check if a key
            if c.islower():
                move_list.append((new_dist, new_row, new_col))
            else:
                new_node_dist = distances.get((new_row, new_col), sys.maxsize)
                if new_dist < new_node_dist:
                    unv_set.append((new_dist, new_row, new_col))
                    distances[(new_row, new_col)] = new_dist

    return move_list

def calc_paths(map, key_list, start_row, start_col):
    # Update map, blocking out the area around the start point, which also
    # has the four entrances.
    map[start_row-1] = map[start_row-1][0:start_col-1] + '.#.' + map[start_row-1][start_col+2:]
    map[start_row] = map[start_row][0:start_col-1] + '###' + map[start_row][start_col+2:]
    map[start_row+1] = map[start_row+1][0:start_col-1] + '.#.' + map[start_row+1][start_col+2:]

    robots = (
        (start_row-1, start_col-1),
        (start_row-1, start_col+1),
        (start_row+1, start_col-1),
        (start_row+1, start_col+1),
    )
    # Key list will be a bitmap
    end_key_set = 2**len(key_list) - 1

    # Set up priority queue for Dijkstra
    visited = set()
    distances = { (robots, 0): 0 }
    unv_set = [ (0, robots, 0) ]

    while unv_set:
        cur_node = heapq.heappop(unv_set)
        cur_robots, cur_keys = cur_node[1], cur_node[2]
        cur_idx = (cur_robots, cur_keys)
        cur_dist = distances[cur_idx]
        visited.add(cur_idx)

        # Stale node
        if cur_node[0] > cur_dist:
            continue

        # Found all the keys?
        if cur_keys == end_key_set:
            return cur_dist

        # For each robot, figure out available keys
        for robot in range(4):
            # Find paths to all keys for this robot
            moves = find_keys(map, cur_keys, cur_robots[robot][0], cur_robots[robot][1])
            for m in moves:
                # Update robot positions with new moved robot
                new_robots = cur_robots[0:robot] + ((m[1], m[2]),) + cur_robots[robot+1:]
                total_dist = cur_dist + m[0]
                c = get_map(map, cur_keys, m[1], m[2])
                new_keys = cur_keys | (1 << ord(c) - ord('a'))
                idx = (new_robots, new_keys)

                # Check if this has been visited yet
                if idx in visited:
                    continue

                new_node = (total_dist, new_robots, new_keys)
                new_node_dist = distances.get(idx, sys.maxsize)
                if total_dist < new_node_dist:
                    distances[idx] = total_dist
                    heapq.heappush(unv_set, new_node)

    print("NO SOLUTION FOUND")
    exit(0)

def main():
    with open(fn, 'r') as file:
        map = [ line.rstrip("\n") for line in file ]
    start_row, start_col = [ (r, line.find('@')) for r, line in enumerate(map) if line.find('@') >= 0 ][0]
    key_list = [ c for line in map for c in line if c.islower() ]

    return calc_paths(map, key_list, start_row, start_col)

answer = main()
print(f"Answer is {answer}")
