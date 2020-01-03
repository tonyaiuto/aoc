#!/usr/bin/env python3

from collections import defaultdict
import copy
import sys

import map


class PlutoMaze(object):

  def __init__(self):
    self.maze = map.Map(label_width=2, open=['.'], ignore=[' '])
    self.jumps = {}
    self.start = None
    self.end = None

  def clone(self):
    ret = PlutoMaze()
    ret.maze = self.maze.clone()
    ret.jumps = dict(self.jumps)
    ret.start = self.start
    ret.end = self.end
    return ret

  def load(self, file):
    # Load the maze and make it ready to work with
    self.maze.load(file)

    label_to_pos = defaultdict(list)
    for pos, label in self.maze.portals.items():
      if label == 'AA':
        self.start = pos
      elif label == 'ZZ':
        self.end = pos
      else:
        label_to_pos[label].append(pos)
    # print(label_to_pos)
    assert self.is_pos_on_edge(self.start)
    assert self.is_pos_on_edge(self.end)
    for l, pairs in label_to_pos.items():
      self.jumps[pairs[0]] = pairs[1]
      self.jumps[pairs[1]] = pairs[0]

    self.maze.close_dead_ends()
    self.maze.print()

    def change_to_walls(pos, v):
      if v and v not in ('#', '.'):
        del self.maze.points[pos]

    self.maze.for_each_cell(change_to_walls)

  def print(self):
    self.maze.print()

  def is_pos_on_edge(self, pos):
    x = pos[0]
    y = pos[1]
    ret = (x == 0 or x == self.maze.width-1
           or y == 0 or y == self.maze.height-1)
    # print('is_pos_on_edge(%s) => %s' % (pos, ret))
    return ret

  def find_min_path(self):
    best_dist = self.maze.width * self.maze.height
    for dist,more in self.walk_path(self.start, self.end, dict(), 0):
      if more == 'end':
        print('got to end in', dist)
        best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, visited, dist):
    while True:
      if pos == end:
        yield dist, 'end'
      visited[pos] = dist
      moves = self.maze.get_moves(pos, visited)
      jump = self.jumps.get(pos)
      if jump and jump not in visited:
        # print('JUMP', jump, self.maze.portals[jump])
        moves.append(jump)
      # print('at', pos, 'dist', dist, 'moves', moves)
      if not moves:
        break
      dist += 1
      if len(moves) == 1:
        pos = moves[0]
        continue
      for branch in moves:
        for n_dist, more in self.walk_path(branch, end, dict(visited), dist):
          yield n_dist, more
      break
    yield -1, 'dead end'


def test_part1():
  maze = PlutoMaze()
  maze.load('sample20_1.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert 23 == best_dist

  maze = PlutoMaze()
  maze.load('sample20_2.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert 58 == best_dist

def part1():
  maze = PlutoMaze()
  maze.load('input_20.txt')
  maze.print()
  print('========================================')
  best_dist = maze.find_min_path()
  print('part1:', best_dist)
  assert 632 == best_dist

  # check that clone works
  m2 = maze.clone()
  best_dist = m2.find_min_path()
  assert 632 == best_dist


class Context(object):

  next_label = defaultdict(int)

  def __init__(self, context=None):
    if context:
      self.visited = copy.deepcopy(context.visited)
      self.in_jumps = set(context.in_jumps)
      self.level = context.level
      self.inbound_labels = copy.deepcopy(context.inbound_labels)
      self.label = '%d.%d=>%s' % (
          self.level, Context.next_label[self.level], context.label)
      self.label = '%d.%d' % (self.level, Context.next_label[self.level])
    else:
      self.visited = {}
      self.visited[0] = {}
      self.in_jumps = set()
      self.inbound_labels = {}
      self.level = 0
      self.label = '%d.%d' % (self.level, Context.next_label[self.level])
    Context.next_label[self.level] += 1

  def ensure_level(self, level):
    if level not in self.visited:
      self.visited[level] = dict()


  def would_recursion_loop(self, label):
    """
    Jump in (40, 23) ('IC', 'RF') to level 19
    =Check for recursion at 12 ['CJ', 'OA', 'XF', 'CK', 'ZH', 'WB', 'IC', 'RF'] in ['AA', 'XF', 'CK', 'ZH', 'WB', 'IC', 'RF', 'NM', 'LP', 'FD', 'XQ', 'RE', 'CJ', 'OA', 'XF', 'CK', 'ZH', 'WB', 'IC']
    =would NOT recurse on (34, 19) ('IC', 'RF')
    would recurse on (34, 19) ('IC', 'RF')
    """

    stack = [self.inbound_labels[i] for i in range(self.level)]
    if len(stack) < 4:
      return False

    pattern = stack[-3:]
    print('=Check for recursion of', pattern, 'in', stack)
    l_targ = len(pattern)
    for start in range(self.level - l_targ - 1):
      if stack[start:start+l_targ] == pattern:
        return True
    return False


class RecursivePlutoMaze(PlutoMaze):

  def __init__(self):
    super(RecursivePlutoMaze, self).__init__()

  def find_min_path(self):

    best_dist = None
    context = Context()
    context.inbound_labels[0] = 'AA'
    for dist,more in self.walk_path(
        self.start, self.end, context, dist=0, depth=0):
      print(dist, more)
      if more == 'end':
        if best_dist is None:
          best_dist = dist
        else:
          best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, context, dist, depth):

    if depth > 50:
      sys.exit(2)
      return

    while True:
      if pos == end and context.level == 0:
        yield dist, '=end'

      context.visited[context.level][pos] = dist
      moves = self.maze.get_moves(pos, context.visited[context.level])

      at_edge = self.is_pos_on_edge(pos)
      jump = self.jumps.get(pos)
      if jump:
        if at_edge:
          if context.level == 0:
            jump = None  # Can not jump out of level 0
          else:
            # Do not backtrack
            if jump in context.visited[context.level-1]:
              jump = None
        else:  # inner jump
          context.ensure_level(context.level+1)
          if jump in context.visited[context.level+1]:
            jump = None

      if not moves and not jump:
        break

      if moves and jump:
        print('====== this Should not happen')
      assert not (moves and jump)

      dist += 1
      if len(moves) == 1 and not jump:
        pos = moves[0]
        continue

      print('at level', context.level, pos, 'dist', dist, 'moves', moves,
            'jump', jump, 'depth', depth, 'context', context.label)

      if jump:
        jump_label = self.maze.portals[jump]
        # context = Context(context)
        if at_edge:
          # outer jump
          context.level -= 1
          print('Jump out', jump, jump_label, 'to level', context.level)
          if context.level == 0 and jump != self.end:
            print('=========== Can not jump out from level 0', pos)
            yield -1, 'jumpout'
            break
        else:
          jtag = (context.inbound_labels[context.level], jump_label)
          context.level += 1
          print('Jump in', jump, jtag, 'to level', context.level)
          if context.would_recursion_loop(jump_label):
            print('=would contxt recurse on', pos, jtag)
            yield -1, 'recurse'
            break
          else:
            print('=would NOT recurse on', pos, jtag)
          if jtag in context.in_jumps:
            print('would recurse on', pos, jtag)
            #yield -1, 'recurse'
            #break
          context.in_jumps.add(jtag)
        context.inbound_labels[context.level] = jump_label
        pos = jump
        continue

      if moves:
        print('=forking context at depth', depth)
        for branch in moves:
          for n_dist, more in self.walk_path(
              branch, end, Context(context), dist, depth=depth+1):
            yield n_dist, more
        return

    yield -1, ('=dead end %s, level %d' % (str(pos), context.level))


def test_part2():
  """
  maze = RecursivePlutoMaze()
  maze.load('sample20_1.txt')
  maze.print()
  assert maze.maze.width == 17
  assert maze.maze.height == 15
  best_dist = maze.find_min_path()
  assert 26 == best_dist

  maze = RecursivePlutoMaze()
  maze.load('sample20_2.txt')
  maze.print()
  best_dist = maze.find_min_path()
  assert None == best_dist
  """

  maze = RecursivePlutoMaze()
  maze.load('sample20_3.txt')
  maze.print()
  best_dist = maze.find_min_path()
  print('sample3 best', best_dist)
  assert -1 == best_dist


def part2():
  maze = PlutoMaze()
  maze.load('input_20.txt')
  maze.print()
  print('========================================')
  best_dist = maze.find_min_path()
  print('part2:', best_dist)
  assert 632 == best_dist


if __name__ == '__main__':
  # test_part1()
  #part1()
  test_part2()
