#!/usr/bin/python
"""Advent of Code 2019, Day 22, Part 1

https://adventofcode.com/2019/day/22

Given a deck of "space cards", apply shuffling techniques and return what
position the card "2019" is in.

See test1.dat-test4.dat for test data and shuffle.dat for full data.

Author: Tim Behrendsen
"""

fn = 'test4.dat'
fn = 'shuffle.dat'

def deal_into_new(deck):
    return list(reversed(deck))

def cut(deck, n):
    return deck[n:] + deck[0:n]

def deal(deck, n):
    size = len(deck)
    new_deck = [0] * size
    for i in range(len(deck)):
        new_deck[(i * n) % size] = deck[i]
    return new_deck

def main():
    testmode = fn[0:4] == 'test'
    deck = range(0, 10 if testmode else 10007)

    with open(fn, 'r') as file:
        for cmd in file:
            cmd = cmd.rstrip("\n")
            if cmd == 'deal into new stack':
                new_deck = deal_into_new(deck)
            elif cmd[0:20] == 'deal with increment ':
                new_deck = deal(deck, int(cmd[20:]))
            elif cmd[0:4] == 'cut ':
                new_deck = cut(deck, int(cmd[4:]))
            else:
                raise Exception(f"Invalid command: {cmd}")

            deck = new_deck

    if testmode:
        return 0
    for i in range(len(deck)):
        if deck[i] == 2019:
            return i

answer = main()
print(f"Answer is {answer}")
