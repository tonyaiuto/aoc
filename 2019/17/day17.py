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


def X(pos):
  return pos[0]

def Y(pos):
  return pos[1]

def all_dirs(pos):
  return [(pos[0], pos[1]-1), (pos[0], pos[1]+1),
          (pos[0]-1, pos[1]), (pos[0]+1, pos[1])]


class VacuumRobot(object):

  def __init__(self, mem):

    self.computer = intcode.IntCode(list(mem))
    self.width = 0
    self.height = 0
    self.scaffold = set()
    self.points = {}
    self.intersections = {}
    self.visited = set()

    """
    self.droid_pos = (0,0)
    self.no_go = set()
    self.oxygen = None
    self.last_dir = 0
    self.span = 0
    self.dist_to_here = {}
    self.min_x = 0
    self.max_x = 0
    self.min_y = 0
    self.max_y = 0

    self.display = None
    self.frame = 0
    self.capture_frames = True
    self.visited.add((0,0))
    self.dist_to_here[(0,0)] = 0
    """

  def get_map(self):
    x = 0
    y = 0
    # line = ''
    while True:
      out = self.computer.run_until_output()
      if self.computer.is_halted:
        break
      c = chr(out)
      if c == '\n':
        y += 1
        x = 0
        # print(line)
        # line = ''
        continue

      # line += c
      self.points[(x, y)] = c
      self.width = max(self.width, x)
      if c == '#':
        self.scaffold.add((x, y))
      x += 1
    self.height = y
  
  def compute_alignment(self):
    alignment = 0
    for pos in self.scaffold:
      is_intersection = True
      for neighbor in all_dirs(pos):
        if not neighbor in self.scaffold:
          is_intersection = False
      if is_intersection:      
        self.intersections[pos] = 'O'
        a = X(pos) * Y(pos)
        print('%s => %d' % (pos, a))
        alignment += a
    return alignment


  def move(self, dir):
    target_pos = move_pos(self.droid_pos, dir)
    if target_pos[0] < self.min_x:
      self.min_x = target_pos[0]
    if target_pos[0] > self.max_x:
      self.max_x = target_pos[0]
    if target_pos[1] < self.min_y:
      self.min_y = target_pos[1]
    if target_pos[1] > self.max_y:
      self.max_y = target_pos[1]
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
      self.points[self.oxygen] = 'O'
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
      if self.frame % 100 == 0:
        print('========= frame %d =============' % self.frame)
        img = ElfImage.fromPoints(self.points)
        img.print()
    print('========= frame %d =============' % self.frame)
    self.points[(0,0)] = 'I'
    img = ElfImage.fromPoints(self.points)
    img.print()

  def finish_map(self):
    max_span = 0
    last_dir = 0
    while len(self.points) < (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1) - 20:
      moves = self.rank_moves()
      if len(moves) == 0:
        break
      dir = moves[0]
      if dir == last_dir and self.span >= last_span and len(moves) > 1:
        dir = move[1]
      self.move(dir)
      self.points[self.oxygen] = 'O'
      self.frame += 1
      if self.frame % 20 == 0:
        print('========= frame %d =============' % self.frame)
        img = ElfImage.fromPoints(self.points)
        img.print()
    print('========= frame %d =============' % self.frame)
    self.points[(0,0)] = 'I'
    img = ElfImage.fromPoints(self.points)
    img.print()


  def o_flood(self):
    gas_edge = [self.oxygen]

    minute = 0
    while len(gas_edge) > 0:
      new_edge = []
      for pos in gas_edge:
        for neighbor in all_dirs(pos):
          if (neighbor[0] < self.min_x
              or neighbor[0] > self.max_x
              or neighbor[1] < self.min_y
              or neighbor[1] > self.max_y):
            continue
          what = self.points.get(neighbor)
          if what == '#' or what == 'O' or what == 'o':
            continue
          if neighbor in self.visited:
            self.points[neighbor] = 'O'
          else:
            self.points[neighbor] = 'o'
          new_edge.append(neighbor)
      if not new_edge:
        break
      gas_edge = new_edge
      minute += 1
      if minute % 20 == 0:
        print('========= minute %d =============' % minute)
        img = ElfImage.fromPoints(self.points)
        img.print()

    print('========= minute %d =============' % minute)
    self.points[(0,0)] = 'I'
    img = ElfImage.fromPoints(self.points)
    img.print()


def part1():
  mem = intcode.load_intcode('input_17.txt')
  robot = VacuumRobot(list(mem))
  robot.get_map()
  img = ElfImage.fromPoints(robot.points)
  img.print(ruler=True)
  print('')
  alignment = robot.compute_alignment()
  img.update(robot.intersections)
  img.print(ruler=True)
  print('part1:', alignment)
  assert 3428 == alignment


def part2():
  mem = intcode.load_intcode('input_17.txt')
  droid = Droid(list(mem))
  droid
  droid.map_to_oxygen()
  droid.finish_map()
  droid.o_flood()
  # 283 is too low.
  # 291 is too hight


if __name__ == '__main__':
  part1()
  # part2()
