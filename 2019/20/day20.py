#!/usr/bin/env python3

from collections import defaultdict
import copy
import sys

import map


class PlutoMaze(object):

  def __init__(self):
    self.maze = map.Map(label_width=2, open=['.'], ignore=[' '])
    # jumps is a table of where you can jump to from this point
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

  def print(self, label=None, visited=None):
    if label:
      print(label)
    overlay =  None
    if visited:
      overlay = {pos: 'v' for pos in visited}
    self.maze.print(overlay=overlay, print_portals=not label)

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
      if more == 'END':
        print('got to end in', dist)
        best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, visited, dist):
    while True:
      if pos == end:
        yield dist, 'END'
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
    yield -1, 'dead end='


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
      self.level = context.level
      self.visited = copy.deepcopy(context.visited)
      self.jump_labels = copy.deepcopy(context.jump_labels)
      self.label = '%d.%d=>%s' % (
          self.level, Context.next_label[self.level], context.label)
      self.label = '%d.%d' % (self.level, Context.next_label[self.level])
      self.parent = context
    else:
      self.visited = [{}]
      self.level = 0
      self.visited[0] = {}
      self.jump_labels = []
      self.label = '%d.%d' % (self.level, Context.next_label[self.level])
      self.parent = None
    Context.next_label[self.level] += 1

  def lineage(self):
    if not self.parent:
      return self.label
    return '%s => %s' % (self.label, self.parent.lineage())

  def ensure_level(self, level):
    for _ in range(level - len(self.visited) + 1):
      self.visited.append(dict())
    # print('ensure_level', level, len(self.visited))
    assert level <= len(self.visited) - 1

  def would_recursion_loop(self, label, indent=''):

    LOOP_DETECT = 4

    stack = self.jump_labels
    if len(stack) < LOOP_DETECT * 2 + 1:
      return False

    last = stack[-1]
    pattern = None
    for targ in range(len(stack)-3, LOOP_DETECT, -1):
      if stack[targ] == label:
        pattern = stack[targ+1:] + [1, label]
        break
    if not pattern:
      return False

    print(indent, '=Check for recursion of', pattern, 'in', stack)
    l_targ = len(pattern)
    for start in range(len(stack) - l_targ * 2 - 2):
      if stack[start:start+l_targ] == pattern:
        repeat = start + l_targ
        if stack[repeat:repeat+l_targ] == pattern:
          return True
    return False


class RecursivePlutoMaze(PlutoMaze):

  def __init__(self):
    super(RecursivePlutoMaze, self).__init__()

  def find_min_path_dfs(self):

    best_dist = None
    context = Context()
    context.jump_labels.append('AA')
    for dist,more in self.walk_path(
        self.start, self.end, context, dist=0, depth=0):
      print(dist, more)
      if more == 'END':
        if best_dist is None:
          best_dist = dist
        else:
          best_dist = min(best_dist, dist)
    return best_dist

  def walk_path(self, pos, end, context, dist, depth):

    # Prevent flame out when I mess up the code.
    if context.level > 20:
      yield -3, 'level='
      return

    indent = '  ' * depth

    jump_label = self.maze.portals.get(pos)
    if jump_label:
      via = 'from %s' % jump_label
      at_edge = self.is_pos_on_edge(pos)
      if at_edge:
        dir = 'recurse into'
      else:
        dir = 'return to'
    else:
      dir = 'branching to'
      via = ''
    print(indent, 'Start walk:', dir,
          'level %d (%s),' % (context.level, context.label),
          'at', pos, 'dist', dist, via, 'depth', depth)

    last_pos = None
    while True:
      if pos == end:
        if context.level == 0:
          yield dist, 'END'
        else:
          yield -1, 'illegal end, level %d, via %s, %s' % (
            context.level, self.maze.portals[pos], pos)

      context.visited[context.level][pos] = dist
      moves = self.maze.get_moves(pos, context.visited[context.level])

      jump = self.jumps.get(pos)
      at_edge = self.is_pos_on_edge(pos)
      if jump and jump == last_pos:
        jump = None
      if jump:
        if at_edge:
          if context.level == 0 and jump != end:
            jump = None  # Can not jump out of level 0
            print(indent, '=can not jump out from level 0', pos)
            yield -1, 'illegal jumpout, level %d, via %s, %s' % (
                context.level, self.maze.portals[pos], pos)
            return
        else:  # inner jump
          context.ensure_level(context.level+1)

      if not moves and not jump:
        break

      if moves and jump:
        print('====== this should not happen')
        print(indent, 'at level', context.level, pos, 'dist', dist,
              'moves', moves, 'jump', jump, 'depth', depth,
              'context',context.label)
      assert not (moves and jump)

      dist += 1
      if len(moves) == 1 and not jump:
        pos = moves[0]
        continue

      print(indent, 'at level', context.level, pos, 'dist', dist,
            'moves', moves, 'jump', jump, 'depth', depth,
            'context',context.label)

      if pos == (21, 5):
        self.print_context_slices(context, level=3)

      if jump:
        dbg_print_level = -1
        if context.level == 3:
          dbg_print_level = 3
        jump_label = self.maze.portals[jump]
        jtag = (context.jump_labels[-1], jump_label)
        if at_edge:
          # outer jump
          print(indent, 'Jump out', jump, jump_label, 'to level', context.level-1)
          if context.level == 0 and jump != self.end:
            print('=========== Can not jump out from level 0', pos)
            yield -1, 'jumpout='
            return
          context.level -= 1
          context.jump_labels.append(0)
        else:
          print(indent, 'Jump in', jump, jump_label, 'to level', context.level+1)
          if context.would_recursion_loop(jump_label, indent=indent):
            print('=would context recurse on', pos, jtag)
            yield -1, 'recurse='
            return
          else:
            print(indent, '=would NOT context recurse on', pos, jtag)
          context.level += 1
          context.jump_labels.append(1)
        context.jump_labels.append(jump_label)

        if context.level == 3:
          dbg_print_level = 3
        if dbg_print_level > 0:
          self.print_context_slice(context, dbg_print_level)

        last_pos = pos
        pos = jump
        continue

      if moves:
        print(indent, '=forking context', context.label, 'at depth', depth)
        for branch in moves:
          for n_dist, more in self.walk_path(
              branch, end, Context(context), dist, depth=depth+1):
            yield n_dist, more
        return

    yield -1, ('=dead end at %s, level %d, context=%s=' % (
               str(pos), context.level, context.label))

  def print_context_slices(self, context, level):
    while context:
      self.print_context_slice(context, level)
      context = context.parent

  def print_context_slice(self, context, level):
    self.print(
        label='\n'.join([
            '====================',
            'Context: %s' % context.lineage(),
            'Layer: %d' % level,
        ]),
        visited=context.visited[level])


  # BFS version
  def find_min_path(self):

    best_dist = None
    context = Context()
    print('look for end at', self.end)

    dist = 0
    level = 0
    heads = [(self.start, level, ('AA', 0))]
    while heads:
      print('==== dist', dist, len(heads), 'heads', heads[0:5])
      new_heads = []
      for (pos, level, level_entry_tag) in sorted(heads, key=lambda x: x[1]):

        context.ensure_level(level)
        prev_d = context.visited[level].get(pos, dist+1)
        if dist >= prev_d:
          print('===reached', pos, level, 'at distances', prev_d, dist)
          # return None
        context.visited[level][pos] = dist
        #print('==set context.visited', pos, level, '=', dist)
        #if len(context.visited) > 3:
        #  if context.visited[3].get((19, 6)):
        #    print('==WTF')

        if pos == self.end and level == 0:
          print('===reached end at', pos, 'dist', dist)
          return dist

        if dist >= 10000:
          print('=== gone too far')
          return None

        jump_label = self.maze.portals.get(pos) or ''
        print(' head', pos, 'level', level, 'dist', dist, jump_label)
        if jump_label == 'RE':
          print('   ======= mark RE', pos, level)

        moves = self.advance(pos, level, dist, level_entry_tag, context)
        if not moves:  # dead end
          continue
        for (n_pos, n_level, _) in moves:
          if n_pos == self.end and n_level == 0:
            print('===will end at', pos, 'dist', dist + 1)
            return dist + 1
        new_heads.extend(moves)
      dist += 1
      heads = new_heads

    print('===ran out of heads')
    return None


  def advance(self, pos, level, dist, level_entry_tag, context):
    moves = self.maze.get_moves(pos, context.visited[level])
    # print(moves)
    jump = self.jumps.get(pos)
    at_edge = self.is_pos_on_edge(pos)

    if jump:
      if at_edge:  # would jump out
        if level == 0 and jump != self.end:
          jump = None  # Can not jump out of level 0
          print('  =can not jump out from level 0', pos)
          jump = None
        if level > 0:
          d = context.visited[level-1].get(jump, dist+1)
          if d < dist:
            print('  =suppress out jump on distance', jump, level-1, d, dist)
            jump = None

      else:  # inner jump
        context.ensure_level(level+1)
        d = context.visited[level+1].get(jump, dist+1)
        if d < dist:
          print('  =suppress in jump on distance', jump, level+1, d, dist)
          jump = None


    if not moves and not jump:
      print('=dead end', pos, level, dist)
      return None

    if moves and jump:
      print('====== this should not happen: moves and jump')
      print('at level', level, pos, 'dist', dist,
            'moves', moves, 'jump', jump)
    assert not (moves and jump)

    #print('at level', level, pos, 'dist', dist,
    #        'moves', moves, 'jump', jump)

    if jump:
      jump_label = self.maze.portals[jump]
      e_name = level_entry_tag[0]
      walk_dist = dist - level_entry_tag[1]
      print('walk from %s to %s (%d steps)' % (e_name, jump_label, walk_dist))
      if at_edge:
        # outer jump
        if level == 0 and jump != self.end:
          print('=========== Can not jump out from level 0', pos)
          return None
        level -= 1
        print('  Jump out', jump, jump_label, 'to level', level)
        print('- Return to level', level, 'through', jump_label)
      else:
        level += 1
        print('  Jump in', jump, jump_label, 'to level', level)
        print('- Recurse into level', level, 'thorugh', jump_label)
      return [(jump, level, (jump_label, dist+1))]

    if moves:
      if len(moves) > 1:
        print('=forking at', pos, level, dist)
      new_heads = [(branch, level, level_entry_tag) for branch in moves]
      print('  return', new_heads)
      return new_heads

    print('=dead end at %s, level %d=' % (str(pos), level))
    return None, 0, None


def test_part2():
  maze = RecursivePlutoMaze()
  maze.load('sample20_1.txt')
  maze.print()
  assert maze.maze.width == 17
  assert maze.maze.height == 15
  best_dist = maze.find_min_path()
  assert 26 == best_dist

  maze = RecursivePlutoMaze()
  maze.load('sample20_2.txt')
  # maze.print()
  best_dist = maze.find_min_path()
  assert None == best_dist

  maze = RecursivePlutoMaze()
  maze.load('sample20_3.txt')
  maze.print()
  best_dist = maze.find_min_path()
  print('sample3 best', best_dist)
  assert 396 <= best_dist


def part2():
  maze = RecursivePlutoMaze()
  maze.load('input_20.txt')
  maze.print()
  print('========================================')
  best_dist = maze.find_min_path()
  print('part2:', best_dist)
  assert 632 <= best_dist
  assert 901 <= best_dist
  assert 7162 == best_dist


if __name__ == '__main__':
  # test_part1()
  #part1()
  # test_part2()
  part2()
