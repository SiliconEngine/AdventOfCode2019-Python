#!/usr/bin/python
"""Advent of Code 2019, Day 22, Part 2

https://adventofcode.com/2019/day/22

Given a deck of "space cards", apply shuffling techniques and return what
position the card "2019" is in.

Second part is just composition of linear polynomials ax+b mod L, where L is length of the deck.

First, convert all shuffling rules into linear polynomial. Remember to compose in reverse order. "deal into new stack" is just negative position. "cut" just adds to b. And "deal with increment" multiplies both a and b by modinv, effectively dividing them, modulo L. modinv(x,n) == pow(x,n-2,n) for prime n is everything you need to remember.

Second, raise polynomial to the number of steps, mod L.

See shuffle.dat for full data.

Author: Tim Behrendsen
"""

fn = 'shuffle.dat'

def main():
    num_cards = 119315717514047
    target_idx = 2020

    # Composition of linear polynormials. y = ax+b mod L
    # "deal into new stack" = negate position
    # "deal with increment" = Multiply a and b by increment
    # "cut"                 = Just add to "b"

    a, b = 1, 0                 # Coefficients
    with open(fn, 'r') as file:
        for cmd in file:
            if cmd == 'deal into new stack\n':
                mult, add = -1, -1
            elif cmd.startswith('deal with increment '):
                mult, add = int(cmd[len('deal with increment '):]), 0
            elif cmd.startswith('cut '):
                mult, add = 1, -int(cmd[len('cut '):])
            # la * (a * x + b) + lb == la * a * x + la*b + lb
            # The `% n` doesn't change the result, but keeps the numbers small.
            a = (a * mult) % num_cards
            b = (b * mult + add) % num_cards

    num_cycles = 101741582076661
    # Now want to effectively run:
    #     la, lb = a, b
    #     a = 1, b = 0
    #     for i in range(num_cycles):
    #         a, b = (a * la) % n, (la * b + lb) % n
    # In essence repeating the above loop num_cycles times

    # For a, this is same as computing (a ** num_cycles) % n, which is in the computable
    # realm with fast exponentiation.
    #
    # For b, this is same as computing ... + a**2 * b + a*b + b
    # == b * (a**(num_cycles-1) + a**(num_cycles) + ... + a + 1) == b * (a**num_cycles - 1)/(a-1)
    # That's again computable, but we need the inverse of a-1 mod n.

    # Fermat's little theorem gives a simple inv:
    def inv(a, n): return pow(a, n-2, n)

    Ma = pow(a, num_cycles, num_cards)
    Mb = (b * (Ma - 1) * inv(a-1, num_cards)) % num_cards

    # This computes "where does 2020 end up", but I want "what is at 2020".
    #print((Ma * c + Mb) % n)

    # So need to invert (2020 - MB) * inv(Ma)
    card = ((target_idx - Mb) * inv(Ma, num_cards)) % num_cards
    return card

answer = main()
print(f"Answer is {answer}")
