#!/usr/bin/python
"""Advent of Code 2019, Day 6, Part 1

https://adventofcode.com/2019/day/6

Given a list of nested "orbits", figure out total number of direct
and indirect orbits.

See test.dat for sample data and map.dat for full data.

Author: Tim Behrendsen
"""

import re

fn = 'test.dat'
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

def main():
    with open(fn, 'r') as file:
        for line in file:
            line = line.rstrip("\n");
            parts = line.split(')');
            o1 = Orbit.get(parts[0])
            o2 = Orbit.get(parts[1])
            o1.add_child(o2)

    # Add up total number of parents for each node
    total = 0
    for o in Orbit.registry.values():
        o2 = o
        while o2.parent != None:
            total += 1
            o2 = o2.parent

    return total

answer = main()
print(f"Answer is {answer}")
