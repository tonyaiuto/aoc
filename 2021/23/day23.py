#!/usr/bin/env python3
"AOC 2021: day 23"

from collections import defaultdict
from collections import deque
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class State(object):

  ext = ['.', 'A', 'B', 'C', 'D']

  blockers = [
    #   0        1        2       3      4      5         6
    [[1],       [],      [],     [2], [2,3], [2,3,4], [2,3,4,5]],
    [[1,2],     [2],     [],     [ ],   [3],   [3,4],   [3,4,5]],
    [[1,2,3],   [2,3],   [3],    [ ],    [],     [4],     [4,5]],
    [[1,2,3,4], [2,3,4], [3,4],  [4],    [],     [ ],       [5]]]

  #r 01 2 3 4 56
  #  ..x.x.x.x..
  #s   0 1 2 3
  DISTS = [
    [3, 2, 2, 4, 6, 8, 9],
    [5, 4, 2, 2, 4, 6, 7],
    [7, 6, 4, 2, 2, 4, 5],
    [9, 8, 6, 4, 2, 2, 3]]

  COSTS = [0, 1, 10, 100, 1000]


  for b in blockers:
    assert len(b) == 7
    for room_set in b:
      for r in room_set:
        assert r < 6

  def __init__(self, stacks, rooms=None):
    self.stacks = copy.copy(stacks)
    self.rooms = rooms or [0,0,0,0,0,0,0]
    self.cost = 100000000
    self.sig = self._sig(self.stacks, self.rooms)
    self.depth = max([len(s) for s in self.stacks])
    self.locked = [0] * 4
    self.final = True
    for si, s in enumerate(self.stacks):
      for d in range(len(s)):
        if s[d] != si+1:
          break
        self.locked[si] = d + 1
      if self.locked[si] != self.depth:
        self.final = False
    if self.final:
      self.print()

  def __str__(self):
    return str(self)

  def _sig(self, stacks, rooms):
    s = '|'.join([','.join([str(p) for p in stacks[s]]) for s in range(4)])
    return s + '|' + ','.join([str(r) for r in rooms])

  @staticmethod
  def from_sig(sig):
    parts = sig.split('|')
    stacks = []
    for sd in parts[0:4]:
      if sd:
        stacks.append([int(n) for n in sd.split(',')])
      else:
        stacks.append([])
    rooms = [int(n) for n in parts[4].split(',')]
    return State(stacks, rooms)

  def print(self, indent=''):
    sx = State.ext
    print(indent, '#############', ' !!!!! FINAL !!!!!' if self.final else '')
    print(indent, '#' + sx[self.rooms[0]] + sx[self.rooms[1]]
          + '.' + sx[self.rooms[2]] + '.' + sx[self.rooms[3]] + '.' + sx[self.rooms[4]]
          + '.' + sx[self.rooms[5]] + sx[self.rooms[6]] + '#')
    print(indent, '###' 
          + sx[self.stacks[0][self.depth-1]] + '#'
          + sx[self.stacks[1][self.depth-1]] + '#' 
          + sx[self.stacks[2][self.depth-1]] + '#' 
          + sx[self.stacks[3][self.depth-1]] + '###')
    for r in range(self.depth-2, -1, -1):
      print(indent, '  #'
            + sx[self.stacks[0][r]] + '#'
            + sx[self.stacks[1][r]] + '#' 
            + sx[self.stacks[2][r]] + '#' 
            + sx[self.stacks[3][r]] + '#')
    print(indent, '   %d %d %d %d' % (self.locked[0], self.locked[1], self.locked[2], self.locked[3]))

  def all_moves(self, verbose=False):
    for si, s in enumerate(self.stacks):
      ls = len(s)
      if ls == 0:
        continue
      for ri in range(7):
        pod = self.rooms[ri]
        if pod != si+1:
          continue
        if self.can_drop_in_stack(ri, si):
          cs = copy.deepcopy(self.stacks)
          cr = copy.copy(self.rooms)
          cr[ri] = 0
          cs[si][self.locked[si]] = pod 
          sig = self._sig(cs, cr)
          if sig == self.sig:
            continue
          cost = (State.DISTS[si][ri] + self.depth - 1 - self.locked[si]) * State.COSTS[pod]
          if verbose:
            print('  can drop ', State.ext[pod], 'from', ri, 'to stack', si, 'at cost', cost)
            print('   ', sig)
          yield sig, cost

      for ri in range(7):
        if self.rooms[ri] != 0:
          continue
        for d in range(self.depth-1, self.locked[si]-1, -1):
          pod = self.stacks[si][d]
          if pod == 0:
            continue
          if self.can_move_to_room(si, ri):
            cs = copy.deepcopy(self.stacks)
            cr = copy.copy(self.rooms)
            cr[ri] = pod
            cs[si][d] = 0
            sig = self._sig(cs, cr)
            if sig == self.sig:
              continue
            if verbose:
              print('can move', State.ext[pod], 'from', si, 'to room', ri)
              print('   ', sig)
            cost = (State.DISTS[si][ri] + self.depth - 1 - d) * State.COSTS[pod]
            yield sig, cost
            break



  def can_move_to_room(self, si, ri):
    for bi in State.blockers[si][ri]:
      if self.rooms[bi] != 0:
        return False
    return True

  def can_drop_in_stack(self, ri, si):
    pod = self.rooms[ri]
    # print("    ============================== try drop", pod, si)
    for p in self.stacks[si]:
      if p != 0 and p != pod:
        return False
    for bi in State.blockers[si][ri]:
      if self.rooms[bi] != 0:
        return False
    return True

class day23(aoc.aoc):


  def __init__(self):
    super(day23, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rows = 0
    #self.what = []
    #for i in range(3):
    #  self.what.append([0] * 11)

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    if not line:
      return
    self.initial = State.from_sig(line)
    print(self.initial.sig)
    self.initial.print()


  def do_line_graphic(self, line):
    if not line:
      return
    if line.startswith('#######'):
      return
    offset = 1 if len(line) < 12 else -1 
    for i, c in enumerate(line):
      if c in ('A', 'B', 'C', 'D'):
        pod = ord(c) - ord('A') + 1 
        self.what[self.rows][offset+i] = pod
    self.rows += 1

  def post_load(self):
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    self.initial.cost = 0

    loop = 0
    visited = set()
    frontier = deque([self.initial])
    fsig = {}
    best_cost = 10000000000
    while len(frontier) > 0:
      loop += 1
      if loop % 10000 == 0:
        print('   loop', loop)
      if loop > 500000:
        print("   LOOP CHECK")
        break
      lf = len(frontier)
      # print('= = = = = ', lf, 'nodes')
      cur = frontier.popleft()
      if lf < 3:
        cur.print()
      any_more = False
      for sig, cost in cur.all_moves(verbose=(lf <= 3)):
        if sig in visited:
          continue
        total_cost = cur.cost + cost
        if len(frontier) < 2:
          print('  to visit', sig, 'at cost', cost, 'total cost', total_cost)
        node = fsig.get(sig)
        if node:
          if total_cost >= node.cost:
            continue
        else:
          node = State.from_sig(sig)
          fsig[node.sig] = node
        any_more = True
        node.cost = total_cost
        if node.final:
          print('==== Final node has cost', node.cost)
          if node.cost < best_cost:
            best_cost = node.cost
        frontier.append(node)
      if not any_more:
        visited.add(cur.sig)

    print("best cost", best_cost)
    return min([x.cost for x in fsig.values() if x.final])


  def part2(self):
    print('===== Start part 2')

    parts = self.initial.sig.split('|')
    t = [int(x) for x in parts[0].split(',')]
    parts[0] = ','.join([str(v) for v in [t[0], 4, 4, t[1]]])
    t = [int(x) for x in parts[1].split(',')]
    parts[1] = ','.join([str(v) for v in [t[0], 2, 3, t[1]]])
    t = [int(x) for x in parts[2].split(',')]
    parts[2] = ','.join([str(v) for v in [t[0], 1, 2, t[1]]])
    t = [int(x) for x in parts[3].split(',')]
    parts[3] = ','.join([str(v) for v in [t[0], 3, 1, t[1]]])
    sig = '|'.join(parts)

    print(sig)
    self.initial = State.from_sig(sig)
    self.initial.print()
    return self.part1()


"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
day23.sample_test("""
1,2|4,3|3,2|1,4|0,0,0,0,0,0,0
""", expect1=12521, expect2=44169)


if __name__ == '__main__':
  day23.run_and_check('input2.txt', expect1=19167, expect2=47665)
