#!/usr/bin/env python3

import sys

import elf_image
import intcode


def X(pos):
  return pos[0]

def Y(pos):
  return pos[1]

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

  def __init__(self, mem, pre_play=None):

    self.computer = intcode.IntCode(
        list(mem),
        get_input=lambda: self.get_joystick())
    # The game didn't run because you didn't put in any quarters.
    # Unfortunately, you did not bring any quarters. Memory address 0
    # represents the number of quarters that have been inserted; set
    # it to 2 to play for free.
    self.computer.poke(0, 2)
    self.pre_play = pre_play
    self.points = {}
    self.high_score = 0
    self.display = None
    self.joy_hist = []
    self.ball = None
    self.auto_play = False
    self.frame = 0
    self.capture_frames = True


  def play(self):
    # The arcade cabinet also has a segment display capable of showing
    # a single number that represents the player's current score. When
    # three output instructions specify X=-1, Y=0, the third output
    # instruction is not a tile; the value instead specifies the new
    # score to show in the segment display. For example, a sequence of
    # output values like -1,0,12345 would show 12345 as the player's
    # current score.

    #                 0    1    2    3    4
    color_to_disp = [' ', '#', 'b', '-', 'o']

    self.keep_going = True
    while self.keep_going:
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
        self.points[pos] = color_to_disp[color]
        if color == 3:  # paddle
          self.paddle = pos
        elif color == 4:  # ball
          self.ball = pos
    if self.capture_frames:
      self.display.toPng('mov/frame%05d.png' % self.frame,
                         legend='Score: %d'  % self.high_score)
    self.frame += 1


  def get_joystick(self):
    # The arcade cabinet has a joystick that can move left and right.
    # The software reads the position of the joystick with input instructions:
    # If the joystick is in the neutral position, provide 0.
    # If the joystick is tilted to the left, provide -1.
    # If the joystick is tilted to the right, provide 1.
    if not self.keep_going:
      return
    if not self.display:
      self.display = elf_image.ElfImage.fromPoints(self.points)
    else:
      self.display.update(self.points)
    self.points = {}
    self.display.print()
    if self.capture_frames:
      self.display.toPng('mov/frame%05d.png' % self.frame,
                         legend='Score: %d'  % self.high_score)
    self.frame += 1
    print('High score:', self.high_score)

    stick = 'n'
    if self.auto_play:
      if X(self.ball) < X(self.paddle):
       stick = 'l'
      elif X(self.ball) > X(self.paddle):
       stick = 'r'
    else:
      if self.pre_play:
        stick = self.pre_play[0]
        self.pre_play = self.pre_play[1:]
      else:
        stick = input('Joystick L, N, R: ').strip()

    stick = (stick or 'n').lower()
    self.joy_hist.append(stick)
    if stick == 'l':
      return -1
    elif stick == 'r':
      return 1
    elif stick == 'q':
      self.keep_going = False
      return 0
    else:
      return 0


def part2(args):
  # Beat the game by breaking all the blocks.
  # What is your score after the last block is broken?

  pre_play=None
  if len(args) > 0:
    with open(args[0], 'r') as inp:
      pre_play = inp.read().strip()

  mem = intcode.load_intcode('input_13.txt')
  game = Game(mem, pre_play=pre_play)
  game.auto_play = True
  game.play()
  with open('stick.txt', 'w') as save:
    save.write(''.join(game.joy_hist))
  print('High score:', game.high_score)


if __name__ == '__main__':
  part1()
  part2(sys.argv[1:])
