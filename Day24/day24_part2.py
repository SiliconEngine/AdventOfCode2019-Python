#!/usr/bin/python
"""Advent of Code 2019, Day 24, Part 2

https://adventofcode.com/2019/day/24

Given a map of bugs, follow rules similar to game-of-life and calculate
the number of bugs after 200 generations. The wrinkle is that the center
square is a recursive level of five squares, and the grid itself is
embedded in another level.

See test.dat for test data and bugs.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test.dat'
fn = 'bugs.dat'

class Eris:
    def __init__(self, lines):
        self.grid = { 0: lines }
        self.low_level = 0
        self.high_level = 0

    def count_bugs(self):
        count = 0
        for level in range(self.low_level, self.high_level+1):
            for row in range(5):
                for col in range(5):
                    count += self.grid[level][row][col] == '#'
        return count

    # Figure out how many adjacent bugs
    def get_adj_count(self, level, row, col):
        # Build a list of adjacent cells
        adj_list = []
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ckrow, ckcol = row+dr, col+dc

            # Check going inward
            if (ckrow, ckcol) == (2, 2):
                if dc == 1:         # Moving right
                    for r in range(5): adj_list.append((level+1, r, 0))
                elif dc == -1:      # Moving left
                    for r in range(5): adj_list.append((level+1, r, 4))
                elif dr == 1:       # Moving down
                    for c in range(5): adj_list.append((level+1, 0, c))
                elif dr == -1:      # Moving up
                    for c in range(5): adj_list.append((level+1, 4, c))
            else:
                # Check going outward
                if ckcol < 0:           # Left side
                    adj_list.append((level-1, 2, 1))
                elif ckcol >= 5:        # Right side
                    adj_list.append((level-1, 2, 3))
                elif ckrow < 0:         # Top
                    adj_list.append((level-1, 1, 2))
                elif ckrow >= 5:        # Bottom
                    adj_list.append((level-1, 3, 2))
                else:                   # Normal coord on level
                    adj_list.append((level, ckrow, ckcol))

        # Count adjacent cells
        count = 0
        for l, r, c in adj_list:
            # See if we need to expand to another dimension
            if l < self.low_level:
                self.grid[l] = [ '.....' ] * 5
                self.low_level = l
            if l > self.high_level:
                self.grid[l] = [ '.....' ] * 5
                self.high_level = l

            count += self.grid[l][r][c] == '#'

        return count

    # Perform a generation of bugs
    def gen_bugs(self):
        levels = (self.low_level-1, self.high_level+1)

        # Construct new grids for each level
        new_grids = { }
        for level in range(self.low_level-1, self.high_level+2):
            new_grid = []
            for row in range(5):
                new_line = []
                for col in range(5):
                    if (row, col) == (2, 2):
                        new_line.append('?')
                        continue
                    count = self.get_adj_count(level, row, col)

                    if self.grid[level][row][col] == '#':
                        new_line.append('#' if count == 1 else '.')
                    else:
                        new_line.append('#' if 1 <= count <= 2 else '.')
                new_grid.append(''.join(new_line))
            new_grids[level] = new_grid

        # Apply the new grids
        for level in range(levels[0], levels[1]+1):
            new_grid = new_grids[level]
            self.grid[level] = new_grid

def main():
    with open(fn, 'r') as file:
        lines = [ line.rstrip("\n") for line in file ]

    eris = Eris(lines)
    for loop in range(200):
        eris.gen_bugs()

    return eris.count_bugs()

answer = main()
print(f"Answer is {answer}")
