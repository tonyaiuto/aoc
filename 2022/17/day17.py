#!/usr/bin/env python3
"AOC 2021: day 17"

from collections import defaultdict
import copy
import heapq
import itertools
import math
import sys

from tools import aoc
from tools import gridutils

SHAPES = """
0123
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


class Rock(object):

  def __init__(self, id, height, width, coords):
    self.id = id
    self.height = height
    self.width = width
    self.coords = coords
    pass

  def __str__(self):
    return str(self)

ROCKS = [
    Rock(id='line',  height=1, width=4, coords=[(0,0), (1,0), (2,0), (3,0)]),
    Rock(id='cross', height=3, width=3, coords=[(1,0), (0,-1), (1,-1), (2,-1), (1,-2)]),
    Rock(id='L',     height=3, width=3, coords=[(2,0), (2,-1), (0,-2), (1,-2), (2,-2)]),
    Rock(id='bar',   height=4, width=1, coords=[(0,0), (0,-1), (0, -2), (0, -3)]),
    Rock(id='box',   height=2, width=2, coords=[(0,0), (1,0), (0,-1), (1,-1)]),
]


class day17(aoc.aoc):

  def __init__(self):
    super(day17, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.rock = 0
    self.grid = gridutils.Grid(default_cell='.')
    self.row_value = {}
    self.top = 0
    self.n_dropped = 0
    self.drop_2_delta = {}
    self.delta_2_drop = defaultdict(list)
    self.drop_2_top = {}

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    self._puffs = self.all_input[0].strip()
    self._next_puff = 0

  def get_puff(self):
    ret = self._puffs[self._next_puff]
    self._next_puff = (self._next_puff + 1) % len(self._puffs)
    return ret

  def show_grid(self, rock, x, y):
    if not self.trace:
      return
    start = max(y, self.top+3)
    i = 0
    for row in aoc.visit_range(start, 0):
      i = i + 1
      if i > 20:
        return
      rc = [self.grid.get(x, row) for x in range(7)]
      if row <= y and row > y-rock.height:
        # maybe splice in some of the rock
        rock_row = y - row
        for c in rock.coords:
          if c[1] == -rock_row:
            while x + c[0] >= len(rc):
              rc.append('x')
            rc[x + c[0]] = '@'
      print('%3d |%s|' % (row, ''.join(rc)))

  def part1(self):
    print('===== Start part 1')
    self.reset()
    return self.run_for(2022)
  
  def run_for(self, limit):
    n_rocks = 0
    for i in range(limit):
      #if self.trace_sample and i % 1000 == 0:
      #  print('rock', i)
      rock, y = self.drop_rock()
      n_rocks += 1
      x = 2
      # print('----- new rock', rock.id)
      # self.show_grid(rock, x, y)

      while True:
        puff = self.get_puff()
        x, y = self.puff_rock(puff, rock, x, y)
        # self.show_grid(rock, x, y)

        # drop it
        if self.collision(rock, x, y-1):
          self.place_rock(rock, x, y)
          # self.show_grid(rock, x, y)
          break
        y = y - 1
        # print('drop to', y)
        # self.show_grid(rock, x, y)
    assert limit == n_rocks
    self.top_index = self.top
    while self.row_value.get(self.top_index, 0) == 0:
      self.top_index -= 1
    self.drop_2_top[self.n_dropped] = self.top_index
    return self.top

  def has_cycle(self):
    if self.top % 2 == 1:
      return false
    h = self.top // 2


  def puff_rock(self, puff, rock, x, y):
    # Puffs rock and returns new x, y
    # print('puff', puff, 'at', x, y, rock.id)
    if puff == '<':
      if x == 0 or self.collision(rock, x-1, y):
        return x, y
      return x-1, y

    assert puff == '>'
    if x + rock.width >= 7 or self.collision(rock, x+1, y):
        return x, y
    return x+1, y

  def place_rock(self, rock, x, y):
    to_compute = set()
    for c in rock.coords:
      self.grid.set(x + c[0], y + c[1], '#')
      to_compute.add(y + c[1])
    self.top = max(self.top, y + 1)
    for row in to_compute:
      n = 0
      for col in range(8):
        b = 1 if (self.grid.get(col, row) == '#') else 0
        n = n << 1 | b
      self.row_value[row] = n
      if n == 127:
        print('  ******** shelf row at: %8d' % row)

  def collision(self, rock, x, y):
    if y - rock.height + 1 < 0:
      print("BOTTOM", y, rock.height)
      return True
    for c in rock.coords:
      if self.grid.get(x + c[0], y + c[1]) == '#':
        # print("COLLIDE")
        return True
    return False

  def drop_rock(self):
    rock = ROCKS[self.rock]
    self.rock = (self.rock + 1) % 5
    self.n_dropped += 1
    return rock, self.top + 3 + rock.height - 1

  def part2(self):
    print('===== Start part 2')
    self.reset()
    # return self.run_for(1000000) 

    goal = 1000000000000
    cycle = len(self._puffs) * 5
    rock = ROCKS[0]

    last_top = 0
    self.cycle = cycle

    loops = goal // self.cycle
    prerun = goal - loops * self.cycle
    print('cycle', self.cycle, 'prerun', prerun)
    if prerun > 0:
       ret = self.run_for(prerun)
       delta = self.top_index - last_top
       last_top = self.top_index
       self.drop_2_delta[self.n_dropped] = delta
       self.delta_2_drop[delta].append(self.n_dropped)

    for i in range(200000):
      if i % 1000 == 0:
        print(i)
      ret = self.run_for(self.cycle)
      for col in range(7):
        assert self.grid.get(col, self.top) == '.'
      delta = self.top_index - last_top
      last_top = self.top_index
      self.drop_2_delta[self.n_dropped] = delta
      self.delta_2_drop[delta].append(self.n_dropped)

      print('drop:', self.n_dropped, 'top:', self.top_index, 'delta from last cycle', delta)
      # self.show_grid(rock, 2, self.top_index+1)

      loop_len, loop_height = self.found_loop(self.n_dropped)
      print("=loop1", self.n_dropped, 'len', loop_len, loop_height)
      if loop_len and loop_len > 0:
        print("LOOP AT", self.n_dropped, 'len', loop_len, loop_height)
        # break

      nloop_len, nloop_height = self.find_loop2()
      print("=loop2", self.n_dropped, 'len', nloop_len, nloop_height)
      if nloop_len and nloop_len > 0:
        print("LOOP2 AT", self.n_dropped, 'len', nloop_len, nloop_height)
        break

      """
      loop_len, loop_height = self.find_loop3()
      if loop_len and loop_len > 0:
        print("LOOP3 AT", self.n_dropped, 'len', loop_len)
        break
      """

    # Now that we have found the loop, verify it and calcuulate base height + loop height
    drops_per_loop = self.cycle * loop_len
    print('== At drop ', self.n_dropped, 'found loop over', loop_len, 'cycles', '(of %d drops)' % drops_per_loop, 'height', loop_height)
    # The top of the previous cycle end
    base_drop = self.n_dropped - drops_per_loop
    base_high = self.drop_2_top[base_drop]
    assert base_high + loop_height == self.drop_2_top[self.n_dropped]

    # SMOKE TEST
    self.show_n_rows('cur_top=%d' % self.top, ti=self.top_index, indent='  ')
    self.show_n_rows('previous top', ti=base_high, indent='  ')

    print(' > starting at drop', self.n_dropped, 'with height', self.top_index,
          'looking back top top', base_high)

    need_loops = (goal - self.n_dropped) // drops_per_loop
    print('  needs', need_loops, 'loopcycles to near goal of', goal)
    total_drop = self.n_dropped + drops_per_loop * need_loops
    print('   %d drops + %d drops/loop * %d loops = %d' % (
        self.n_dropped, drops_per_loop, need_loops, total_drop))
    high = self.top_index + need_loops * loop_height
    need_drops = goal - total_drop
    print('  => after', total_drop, 'height would be', high, 'Need %d drops' % need_drops)
    print('   %d = %d high + %d loops * %d high/loop' % (
        high, self.top_index, need_loops, loop_height))

    exp = 1514285714288   # part2 sample expectation
    for i in range(10):
      next_loop_phase = base_drop + cycle * i
      more_h = self.drop_2_delta[next_loop_phase]
      total_drop += cycle
      high += more_h
      need_drops = goal - total_drop
      print('After', total_drop, 'height would be', high, 'Need %d drops' % need_drops)
      print('  part2 sample expect', exp, 'need', exp - high)
      if need_drops == 0:
        # high -= 1
        break
    return high

  def show_n_rows(self, label, ti, n_rows=8, indent=''):
    print(indent + label, 'at', ti)
    for row in range(n_rows):
      v = self.row_value.get(ti - row, 'na')
      print(indent + '  ', ''.join([self.grid.get(col, ti-row) for col in range(7)]), '%3d' % v)


  def found_loop(self, drop):
    delta = self.drop_2_delta[drop]
    possible_matches = self.delta_2_drop[delta]
    # print(possible_matches)
    if len(possible_matches) < 2:
      return None, None
    for nback in range(2, len(possible_matches)+1):
      back_drop = possible_matches[-nback]
      if back_drop + self.cycle == drop:
        continue
      print("=== Check drop", drop, 'back to drop', back_drop)
      target, lspan = self.sum_span(drop, back_drop)
      drops_loop = self.cycle*lspan
      print('  ', lspan, 'cycles back from drop', drop, 'delta_h', target)
      next_back, ls2 = self.sum_span(back_drop, back_drop-drops_loop)
      print('  ', ls2, 'cycles back from drop', back_drop, 'delta_h', next_back)

      if target == next_back and lspan == ls2:
        print("MAYBE WINNER")

        top1 = self.drop_2_top[drop] - target
        top2 = self.drop_2_top[back_drop] - target 
        same = True
        for ri in range(min(target, 100000)):
          if self.row_value[top1 + ri] != self.row_value[top2 + ri]:
            print("Stacks not the same at", top1+ri)
            same = False
            break
        if same:
          print("WINNER")
          return lspan, target
        if not self.trace_sample:
          sys.exit(1)
       
        """
        # make sure 3 in a row match
        if back_drop-drops_loop*2 <= 0:
          print('too soon')
          continue
        nb3, ls3 = self.sum_span(back_drop-drops_loop, back_drop-drops_loop*2)
        print('  ', ls3, 'cycles back from drop', back_drop-drops_loop, 'delta_h', nb3)
        if target == nb3 and lspan == ls3:
          print("WINNER")
          return lspan, target
        """

        """
        h3 = 0
        nb3 = back_drop - 2*drops_loop
        xnb3 = nb3
        print("Checking from drop", nb3)
        for i in range(lspan):
          if nb3 <= 0:
            break
          h3 += self.drop_2_delta[nb3]
          nb3 += self.cycle
          print('  ', nb3, h3)
        print('  ', lspan, 'cycles forward from drop', xnb3, 'delta_h', h3)
        if target == h3:
          print("WINNER")
          return lspan, target
        """
    return None, None

  def sum_span(self, drop, back_to_drop):
    ret = 0
    lspan = 0
    while drop > back_to_drop and drop > 0:
      ret += self.drop_2_delta[drop]
      drop -= self.cycle
      lspan += 1
    return ret, lspan

  def find_loop2(self):
    # Try to look backwards N*cycle drops for top of stacks matching.
    # This does not do it for input data.
    if self.n_dropped < self.cycle * 3:
      return None, None

    # ti = self.top_index
    top_drop = self.n_dropped
    lvec = 20
    for nc in range(1, 10):
      if self.n_dropped < nc * self.cycle * 3:
        return None, None

      top_row_index = self.drop_2_top[top_drop]
      offset = nc * self.cycle
      back_drop = top_drop - offset
      back_row_index = self.drop_2_top[back_drop]
      print('Trying match', lvec, 'rows from drop', top_drop, '(h:%d)' % top_row_index,
            'back', nc, 'cycles to drop', back_drop, '(h:%d)' % back_row_index)
      for i in range(self.cycle):  # ?? offset?
        cycle_height = top_row_index - back_row_index
        if self.vec_match(top_row_index, back_row_index, lvec):
          print('## matched', lvec, 'rows at', top_row_index,
                'expected height', cycle_height)
          # verify on next batch down
          next_back_drop = back_drop - offset
          next_back_row_index = self.drop_2_top[next_back_drop]
          if cycle_height != back_row_index - next_back_row_index:
            print('  >> but the hight from next cycles back is ',
                  back_row_index - next_back_row_index)
          else:
            # ??? XXX if lvec == offset:
            return nc, cycle_height
        top_row_index -= 1
        back_row_index -= 1
    return None, None

  def vec_match(self, p1, p2, nv):
    # Match nv values backwards from two offsets
    for i in range(nv):
      if self.row_value[p1 - i] != self.row_value[p2 - i]:
        return False
    return True

  def find_loop3(self):
    if self.n_dropped < self.cycle * 5:
      return None, None

    for nc in range(1, 100):
      offset = nc * self.cycle
      if drop < nc * self.cycle * 3:
        return None, None

      print('Trying for loop over', nc, 'cycles')
      for i in range(self.cycle):  # ?? offset?
        test_top = drop - 1
        if self.vec_match(test_top - offset, test_top - 2 * offset, offset):
          print('## matched', offset, 'rows at', test_top - offset)
    return None, None



day17.sample_test("""
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""", expect1=3068, expect2=15142857142889)


if __name__ == '__main__':
  day17.run_and_check('input.txt', expect1=3179, expect2=None)
