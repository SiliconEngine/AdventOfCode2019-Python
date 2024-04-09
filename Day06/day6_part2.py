#!/usr/bin/python
"""Advent of Code 2019, Day 6, Part 2

https://adventofcode.com/2019/day/6

Given a list of nested "orbits", figure out how many orbits we need
to move up the tree from "YOU" and down the tree to SAN (Santa).

See test.dat for sample data and map.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test2.dat'
fn = 'map.dat'

class Orbit:
    registry = { }

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        Orbit.registry[name] = self

    @staticmethod
    def get(name):
        o = Orbit.registry.get(name)
        if o == None:
            o = Orbit(name)
            Orbit.registry[name] = o
        return o

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def __repr__(self):
        return f"[{self.name}, parent = {self.parent.name if self.parent != None else 'None'}]"

def get_parents(node):
    parents = []
    while node != None:
        parents.append(node.name);
        node = node.parent
    return parents

def main():
    with open(fn, 'r') as file:
        for line in file:
            parts = line.rstrip("\n").split(')');
            o1 = Orbit.get(parts[0])
            o2 = Orbit.get(parts[1])
            o1.add_child(o2)

    you = get_parents(Orbit.get('YOU'))
    san = get_parents(Orbit.get('SAN'))

    # Find common branch point, COM is at end
    i = -1
    while you[i] == san[i]:
        i -= 1

    # Figure out how far from branch point we are for both
    i1 = len(you) + i
    i2 = len(san) + i

    # Answer is sum of two distances
    return i1 + i2

answer = main()
print(f"Answer is {answer}")
