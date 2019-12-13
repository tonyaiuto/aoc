#!/usr/bin/env python3

import elf_image
import intcode


def paint(computer):
  points = {}
  while True:
    x = computer.run_until_output()
    if computer.is_halted:
      break
    y = computer.run_until_output()
    color = computer.run_until_output()
    # print(x, y, color)
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
  ic = intcode.IntCode(list(mem))
  points = paint(ic)
  nblocks = 0
  for pos, color in points.items():
    if color == 2:
      nblocks += 1
  print('part1: # blocks:', nblocks)
  assert 280 == nblocks


class Game(object):

  def __init__(self, mem):

    self.computer = intcode.IntCode(
        list(mem),
        get_input=lambda: self.get_joystick())
    # The game didn't run because you didn't put in any quarters.
    # Unfortunately, you did not bring any quarters. Memory address 0
    # represents the number of quarters that have been inserted; set
    # it to 2 to play for free.
    self.computer.poke(0, 2)
    self.points = {}
    self.high_score = 0
    self.display = None

  def play(self):
    # The arcade cabinet also has a segment display capable of showing
    # a single number that represents the player's current score. When
    # three output instructions specify X=-1, Y=0, the third output
    # instruction is not a tile; the value instead specifies the new
    # score to show in the segment display. For example, a sequence of
    # output values like -1,0,12345 would show 12345 as the player's
    # current score.

    color_to_disp = [' ', '#', 'b', '-', 'o']

    while True:
      x = self.computer.run_until_output()
      if self.computer.is_halted:
        break
      y = self.computer.run_until_output()
      color = self.computer.run_until_output()
      pos = (x, y)
      if pos == (-1, 0):
        # color is score
        print('new score:', color)
        self.high_score = max(self.high_score, color)
      else:
        if pos in self.points:
          print("repaint!", pos)
        self.points[pos] = color_to_disp[color]

  def get_joystick(self):
    # The arcade cabinet has a joystick that can move left and right.
    # The software reads the position of the joystick with input instructions:
    # If the joystick is in the neutral position, provide 0.
    # If the joystick is tilted to the left, provide -1.
    # If the joystick is tilted to the right, provide 1.
    if not self.display:
      self.display = elf_image.ElfImage.fromPoints(self.points)
    else:
      self.display.update(self.points)
    self.points = {}
    self.display.print()
    stick = input('Joystick L, N, R: ')
    if stick.lower() == 'l':
      return -1
    elif stick.lower() == 'r':
      return 1
    else:
      return 0


def part2():
  mem = intcode.load_intcode('input_13.txt')
  game = Game(mem)
  game.play()

  # Beat the game by breaking all the blocks.
  # What is your score after the last block is broken?

if __name__ == '__main__':
  part1()
  part2()
