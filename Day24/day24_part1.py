#!/usr/bin/python
"""Advent of Code 2019, Day 24, Part 1

https://adventofcode.com/2019/day/24

Given a map of bugs, follow rules similar to game-of-life and calculate
a "rating" based on the number of bugs once a pattern is generated
that repeats a prior pattern

See test.dat for test data and bugs.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'bugs.dat'

def calc_rating(grid):
    rating = 0
    for row in range(5):
        for col in range(5):
            if grid[row][col] == '#':
                rating += 2 ** (row * 5 + col)
    return rating

def main():
    with open(fn, 'r') as file:
        grid = [ line.rstrip("\n") for line in file ]

    chk_set = set()
    while True:
        new_grid = []
        for row in range(5):
            new_line = []
            for col in range(5):
                count = 0
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ckrow, ckcol = row+dr, col+dc
                    if 0 <= ckrow < 5 and 0 <= ckcol < 5:
                        count += grid[ckrow][ckcol] == '#'

                if grid[row][col] == '#':
                    new_line.append('#' if count == 1 else '.')
                else:
                    new_line.append('#' if 1 <= count <= 2 else '.')
            new_grid.append(''.join(new_line))

        # Check if this new grid repeats a prior grid
        grid = new_grid
        key = ''.join(grid)
        if key in chk_set:
            return calc_rating(grid)

        chk_set.add(key)

    return 0

answer = main()
print(f"Answer is {answer}")
