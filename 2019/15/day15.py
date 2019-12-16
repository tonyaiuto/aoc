#!/usr/bin/env python3

import sys

from elf_image import ElfImage
import intcode


def move_pos(pos, dir):
  if dir == 1:
    return (pos[0], pos[1]-1)
  elif dir == 2:
    return (pos[0], pos[1]+1)
  elif dir == 3:
    return (pos[0]-1, pos[1])
  elif dir == 4:
    return (pos[0]+1, pos[1])
  else:
    raise Exception('invalid direction: %d' % dir)


def all_dirs(pos):
  return [(pos[0], pos[1]-1), (pos[0], pos[1]+1),
          (pos[0]-1, pos[1]), (pos[0]+1, pos[1])]


class Droid(object):

  def __init__(self, mem):

    self.computer = intcode.IntCode(list(mem))

    self.droid_pos = (0,0)
    self.no_go = set()
    self.visited = set()
    self.oxygen = None
    self.last_dir = 0
    self.span = 0
    self.points = {}
    self.dist_to_here = {}

    self.display = None
    self.frame = 0
    self.capture_frames = True
    self.visited.add((0,0))
    self.dist_to_here[(0,0)] = 0


  def move(self, dir):
    target_pos = move_pos(self.droid_pos, dir)
    self.computer.push_input(dir)
    status = self.computer.run_until_output()
    if status == 0:
      self.points[target_pos] = '#'
      self.no_go.add(target_pos)
      return False
    self.visited.add(target_pos)
    self.points[self.droid_pos] = '.'
    self.droid_pos = target_pos
    self.points[self.droid_pos] = 'D'

    min_dist = 999999999
    for neighbor in all_dirs(target_pos):
      if not neighbor in self.visited:
        continue
      dist = self.dist_to_here[neighbor]
      if dist < min_dist:
        min_dist = dist
    self.dist_to_here[target_pos] = 1 + min_dist

    if self.last_dir == dir:
      self.span += 1
    else:
      self.span = 0
    self.last_dir = dir
    if status == 2:
      self.oxygen = target_pos
      self.points[target_pos] = 'O'
      print('dist to oxygen', self.dist_to_here[target_pos])
    return True

  def rank_moves(self):
    unexplored = []
    visited = []
    for dir in range(1, 5):
      target_pos = move_pos(self.droid_pos, dir)
      if target_pos in self.no_go:
        continue
      elif target_pos in self.visited:
        visited.append(dir)
      else:
        unexplored.append(dir)
    ret = unexplored + visited
    if len(ret) == 1:  # dead end
      self.no_go.add(self.droid_pos)
    return ret

  def map_to_oxygen(self):

    max_span = 0
    last_dir = 0
    while not self.oxygen:
      moves = self.rank_moves()
      dir = moves[0]
      if dir == last_dir and self.span >= last_span and len(moves) > 1:
        dir = move[1]
      self.move(dir)
      self.frame += 1
      if self.frame % 20 == 0:
        print('=======================================')
        img = ElfImage.fromPoints(self.points)
        img.print()
    print('=======================================')
    self.points[(0,0)] = 'I'
    img = ElfImage.fromPoints(self.points)
    img.print()


def part1():
  mem = intcode.load_intcode('input_15.txt')
  droid = Droid(list(mem))
  droid.map_to_oxygen()


def part2(args):
  # Beat the game by breaking all the blocks.
  # What is your score after the last block is broken?

  mem = intcode.load_intcode('input_13.txt')
  game = Game(mem)
  game.play()


if __name__ == '__main__':
  part1()
  # part2(sys.argv[1:])
