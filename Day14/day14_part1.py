#!/usr/bin/python
"""Advent of Code 2019, Day 14, Part 1

https://adventofcode.com/2019/day/14

Given a set of "reactions" for turning a list of ingredients into another
chemical, figure out the minimum amount of "ore" needed to produce one
unit of fuel.

See test*.dat for test data and reactions.dat for full data.

Author: Tim Behrendsen
"""

fn = 'testx.dat'
fn = 'test4.dat'
fn = 'reactions.dat'

import re
import math

class Reaction:
    registry = { }

    @staticmethod
    def make(name, qty, ing_list):
        return Reaction(qty, name, ing_list)

    @staticmethod
    def get(name):
        return Reaction.registry[name]

    def __init__(self, name, qty, ing_list):
        self.name = name
        self.qty = qty
        self.ing_list = ing_list
        Reaction.registry[name] = self

def calc_amount(start_qty, start_name):
    # First create plan, which is the order that materials are processed
    q = [ start_name ]
    plan = []
    while len(q) != 0:
        out_name = q.pop(0)
        if out_name == 'ORE':
            continue
        plan.append(out_name)
        r = Reaction.get(out_name)
        for ing_qty, ing_name in r.ing_list:
            q.append(ing_name)

    # The plan that was created may have materials in multiple spots. We want
    # a new list that defers a material until it's used be everything. Scan the
    # list, keeping the furthest occurance of each.
    temp_plan = []
    for name in reversed(plan):
        if name not in temp_plan:
            temp_plan.append(name)
    plan = reversed(temp_plan)

    # Execute plan, processing each one in order, accumulating how much
    # of each one we need.
    need_amts = { start_name: start_qty }
    for out_name in plan:
        # Process this material
        r = Reaction.get(out_name)
        out_qty = r.qty

        # Scan each ingredient, figuring out how much we need. Batches can't
        # be split, so we have to round up.
        for ing_qty, ing_name in r.ing_list:
            batch_qty = math.ceil(need_amts[out_name] / out_qty)
            amt_needed = batch_qty * ing_qty
            need_amts[ing_name] = need_amts.get(ing_name, 0) + amt_needed

    return need_amts['ORE']

def main():
    with open(fn, 'r') as file:
        for line in file:
            left, right = line.rstrip("\n").split(' => ')
            output = right.split(' ')

            left_list = left.split(", ")
            ing_list = [ [int(item[0]), item[1] ] for item in (s.split(' ') for s in left_list) ]
            Reaction.make(int(output[0]), output[1], ing_list)

    return calc_amount(1, 'FUEL')

answer = main()
print(f"Answer is {answer}")
