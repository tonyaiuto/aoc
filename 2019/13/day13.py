#!/usr/bin/env python3

import intcode


def paint(computer):
  points = {}
  while True:
    x = computer.run_until_output()
    if computer.is_halted:
      break
    y = computer.run_until_output()
    color = computer.run_until_output()
    print(x, y, color)
    pos = (x, y)
    if pos in points:
      print("repaint!", pos)
    points[pos] = color
  return points


def part1():
  # The arcade cabinet runs Intcode software like the game the
  # Elves sent (your puzzle input). It has a primitive screen capable
  # of drawing square tiles on a grid. The software draws tiles to
  # the screen with output instructions: every three output
  # instructions specify the x position (distance from the left),
  # y position (distance from the top), and tile id. The tile id
  # is interpreted as follows:

  # 0 is an empty tile. No game object appears in this tile.
  # 1 is a wall tile. Walls are indestructible barriers.
  # 2 is a block tile. Blocks can be broken by the ball.
  # 3 is a horizontal paddle tile. The paddle is indestructible.
  # 4 is a ball tile. The ball moves diagonally and bounces off objects.

  # For example, a sequence of output values like 1,2,3,6,5,4
  # would draw a horizontal paddle tile (1 tile from the left and 2 tiles
  # from the top) and a ball tile (6 tiles from the left and 5 tiles
  # from the top).

  # BOOST keycode does it produce?
  mem = intcode.load_intcode('input_13.txt')
  ic = intcode.IntCode(list(mem), input=[1])
  points = paint(ic)
  nblocks = 0
  for pos, color in points.items():
    if color == 2:
      nblocks += 1
  print('part1: # blocks:', nblocks)
  assert 280 == nblocks


def part2():
  pass

if __name__ == '__main__':
  part1()
  part2()
