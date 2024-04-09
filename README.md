# Advent of Code 2019 solutions written in Python.
## Author: Tim Behrendsen

Link: https://adventofcode.com/2019/

Advent of Code is a series of puzzles over 25 days, each with a part 1 and
part 2. The difficulty roughly rises each day, with the later puzzles often
requiring some tricky algorithms to solve.

For these solutions, the various days are in separate directories, with a
separate file for each part. Day 25, as traditional, is only a single part.

### Advent of Code 2019, Day 1, Part 1

Link: https://adventofcode.com/2019/day/1

Sum "fuel requirements" for list of module masses using a simple formula.

### Advent of Code 2019, Day 1, Part 2

Link: https://adventofcode.com/2019/day/1

Sum "fuel requirements" for list of module masses using a simple formula.
Part 2 requires adding in fuel required for the mass of the fuel, in a
recursive loop (module + [weight of fuel] + [weight of that fuel] + ...)

### Advent of Code 2019, Day 2, Part 1

Link: https://adventofcode.com/2019/day/2

Interpret simple program commands and display result.

### Advent of Code 2019, Day 2, Part 2

Link: https://adventofcode.com/2019/day/2

Interpret simple program commands, and search for combination of
parameters that return 19690720.

### Advent of Code 2019, Day 3, Part 1

Link: https://adventofcode.com/2019/day/3

Figure out intersection points of a pair of paths and find minimum manhattan
distance of which point from origin.

### Advent of Code 2019, Day 3, Part 2

Link: https://adventofcode.com/2019/day/3

Figure out intersection points of a pair of paths and find minimum distance
to intersecting points from origin.

### Advent of Code 2019, Day 4, Part 1

Link: https://adventofcode.com/2019/day/4

Compute how many passwords fit a criteria within a numeric range.

### Advent of Code 2019, Day 4, Part 2

Link: https://adventofcode.com/2019/day/4

Compute how many passwords fit a criteria within a numeric range.

### Advent of Code 2019, Day 5, Part 1

Link: https://adventofcode.com/2019/day/5

Interpret simple program commands, and run "diagnostics". Implements
different access modes in instruction codes.

### Advent of Code 2019, Day 5, Part 2

Link: https://adventofcode.com/2019/day/5

Interpret simple program commands, and run "diagnostics". Implements
different access modes in instruction codes, and adds new instructions.

### Advent of Code 2019, Day 6, Part 1

Link: https://adventofcode.com/2019/day/6

Given a list of nested "orbits", figure out total number of direct
and indirect orbits.

### Advent of Code 2019, Day 6, Part 2

Link: https://adventofcode.com/2019/day/6

Given a list of nested "orbits", figure out how many orbits we need
to move up the tree from "YOU" and down the tree to SAN (Santa).

### Advent of Code 2019, Day 7, Part 1

Link: https://adventofcode.com/2019/day/7

Uses "intcode" computer from prior days. Find the highest "thrust"
value by finding the optimal combination of input values that produces
the highest number.

### Advent of Code 2019, Day 7, Part 2

Link: https://adventofcode.com/2019/day/7

Uses "intcode" computer from prior days, but in this variation, it has
to maintain five running versions of it, each one stopping when it outputs
a number, which gets fed to the next one in the chain. This continues until
it hits a stop instruction.

This was a perfect opportunity to use the Python 'yield/next' feature.

### Advent of Code 2019, Day 8, Part 1

Link: https://adventofcode.com/2019/day/8

Decode an image that consists of a series of layers. Find the one
with the fewest '0' pixels, and the multiply the number of '1' and '2'
pixels.

### Advent of Code 2019, Day 8, Part 2

Link: https://adventofcode.com/2019/day/8

Decode an image, where each pixel is the first black/white pixel below
transparent pixels in a series of layers.

### Advent of Code 2019, Day 9, Part 1 and Part 2

Link: https://adventofcode.com/2019/day/9

Uses "intcode" computer from prior days. Adds a new "relative mode" for addressing.

### Advent of Code 2019, Day 10, Part 1

Link: https://adventofcode.com/2019/day/10

Given a map of "asteroids", figure out which asteroid has the most
asteroids in sight, without one occluding another (at same angle).

### Advent of Code 2019, Day 10, Part 2

Link: https://adventofcode.com/2019/day/10

Given a map of "asteroids", figure out which asteroid has the most
asteroids in sight, without one occluding another (at same angle).
From there, start destroying asteroids one at a time with a laser
starting directly straight up in a circle. Compute which asteroid will
be the 200th one destroyed (after removing ones in the way).

### Advent of Code 2019, Day 11, Part 1 and 2

Link: https://adventofcode.com/2019/day/11

Uses "intcode" computer from prior days. Given a painting program for the intcode
computer, first calculate the number of squares painted, then figure out what
letters are generated.

### Advent of Code 2019, Day 12, Part 1

Link: https://adventofcode.com/2019/day/12

Given a set of integer positions for "moons", simulate gravity according to
some simple rules. Calculate the final "energy".

### Advent of Code 2019, Day 12, Part 2

Link: https://adventofcode.com/2019/day/12

Given a set of integer positions for "moons", simulate gravity according to
some simple rules. In part 2, we calculate how many cycles until the moons
return to their original position. Required detecting patterns in the positions
and then using a least-common-multiple.

### Advent of Code 2019, Day 13, Part 1 and 2

Link: https://adventofcode.com/2019/day/13

Uses "intcode" computer from prior days. Given an intcode program that plays
breakout, figure out number of blocks to clear, then play the game and return
final score.

### Advent of Code 2019, Day 14, Part 1

Link: https://adventofcode.com/2019/day/14

Given a set of "reactions" for turning a list of ingredients into another
chemical, figure out the minimum amount of "ore" needed to produce one
unit of fuel.

### Advent of Code 2019, Day 14, Part 2

Link: https://adventofcode.com/2019/day/14

Given a set of "reactions" for turning a list of ingredients into another
chemical, figure out the how much fuel can be produced with one trillion units
of ore. It turned out that this could be solved by just changing the calculation
to floating point and dividing it out. This may not work for all input data, but
I suspect the puzzle was designed to allow this easy solution.

### Advent of Code 2019, Day 15, Part 1 and 2

Link: https://adventofcode.com/2019/day/15

Uses "intcode" computer from prior days. An IntCode program controls a robot,
and needs to find an "oxygen system". Part 1 finds the oxygen system and
computes the number of steps. Part 2 computes the time taken for oxygen
to fill the space, which is basically the longest path.

The IntCode computer now has a save / restore state, which saved having to
implementing backtracking on the robot.

### Advent of Code 2019, Day 16, Part 1

Link: https://adventofcode.com/2019/day/16

Given a list of "signal" digits, apply a transformation algorithm and repeat 100 times.
The tricky part is a pattern is applied, which itself is modified based on the position
in the digit list.

### Advent of Code 2019, Day 16, Part 2

Link: https://adventofcode.com/2019/day/16

Given a list of "signal" digits, repeat the digits 10,000 times and then apply
the transformation algorithm 100 times from part 1. Using the first 7 digits, use
that as the offset to return the 8 digits at that offset.

Because of the way the pattern is applied, it turns out that last 25% of the digits
follow a pattern of: digit [n] = sum(digits[n .. end]) % 10. Once that's figured
out, it's a simple matter to solve since the offset towards the end.

### Advent of Code 2019, Day 17, Part 1 and 2

Link: https://adventofcode.com/2019/day/17

Uses "intcode" computer from prior days. Guide a "cleaning robot" across scaffolding,
giving it a sequence of movement commands, based on a "video feed". The movement
commands must fit within a certain string length, so requires finding a specific
solution that fits the constraints.

### Advent of Code 2019, Day 18, Part 1

Link: https://adventofcode.com/2019/day/18

Given a map with doors and keys that must be visited, find the shortest path
to gather the keys and unlock the doors. Uses Dijkstra with coordinates and
the set of gathered keys.

### Advent of Code 2019, Day 18, Part 2

Link: https://adventofcode.com/2019/day/18

Given a map with doors and keys that must be visited, find the shortest path
to gather the keys and unlock the doors. In part 2, we have for robots that
traverse isolated quadrants of the map. Uses two Dijkstra searches, an
inner one that figures out what keys are traversable, and then an outer main
Dijkstra that uses the key coordinates + current keys gathered.

### Advent of Code 2019, Day 19, Part 1 and 2

Link: https://adventofcode.com/2019/day/19

Uses "intcode" computer from prior days. Program is a "drone" that can return
whether a particular point is within a "tractor beam". Part 1 is counting
the number of beam squares within a 50x50 grid. Part 2 is figuring out the
closest point where a 100x100 square fill fit within the beam.

### Advent of Code 2019, Day 20, Part 1

Link: https://adventofcode.com/2019/day/20

Given a map with teleportation gates, calculate the shortest path. Uses Dijkstra
to calculate the path. Trickiest part was extracting the gates, which are marked
with sequences of two letters, left-to-right or north-to-south.

### Advent of Code 2019, Day 20, Part 2

Link: https://adventofcode.com/2019/day/20

Given a map with teleportation gates, calculate the shortest path. Uses Dijkstra
to calculate the path. Trickiest part was extracting the gates, which are marked
with sequences of two letters, left-to-right or north-to-south. For Part 2, the
gates transfer to a recursive "inner area", which means it needed a third
dimension coordinate for the path search.

### Advent of Code 2019, Day 21, Part 1 and 2

Link: https://adventofcode.com/2019/day/21

Uses "intcode" computer from prior days. Given a jumping robot equipped with hole
sensors, we must give it a sequence of boolean instructions to navigate over a 1D
terrain. Required getting a little further and analyzing what rules would jump over
the holes of different sizes.

### Advent of Code 2019, Day 22, Part 1

Link: https://adventofcode.com/2019/day/22

Given a deck of "space cards", apply shuffling techniques and return what
position the card "2019" is in.

### Advent of Code 2019, Day 22, Part 2

Link: https://adventofcode.com/2019/day/22

Given a deck of "space cards", apply shuffling techniques and return what
position the card "2019" is in.

Second part is just composition of linear polynomials ax+b mod L, where L is length of the deck.

First, convert all shuffling rules into linear polynomial. Remember to compose in reverse order. "deal into new stack" is just negative position. "cut" just adds to b. And "deal with increment" multiplies both a and b by modinv, effectively dividing them, modulo L. modinv(x,n) == pow(x,n-2,n) for prime n is everything you need to remember.

Second, raise polynomial to the number of steps, mod L.

### Advent of Code 2019, Day 23, Part 1 and 2

Link: https://adventofcode.com/2019/day/23

### Advent of Code 2019, Day 24, Part 1

Link: https://adventofcode.com/2019/day/24

Given a map of bugs, follow rules similar to game-of-life and calculate
a "rating" based on the number of bugs once a pattern is generated
that repeats a prior pattern

### Advent of Code 2019, Day 24, Part 2

Link: https://adventofcode.com/2019/day/24

Given a map of bugs, follow rules similar to game-of-life and calculate
the number of bugs after 200 generations. The wrinkle is that the center
square is a recursive level of five squares, and the grid itself is
embedded in another level.

### Advent of Code 2019, Day 25

Link: https://adventofcode.com/2019/day/25

Uses "intcode" computer from prior days. Plays an interactive "adventure" game
and has to find a combination of picked-up items that allows moving past a
security checkpoint. It automatically navigates the map, accumulates the items
and tries combinations of items until it gets past the security checkpoint.

