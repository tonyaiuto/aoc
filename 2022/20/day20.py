#!/usr/bin/env python3
"AOC 2021: day 20"

from collections import defaultdict
import copy

from tools import aoc


TRACE=1


def order_to_list(order):
  v_p = [(v, p)
         for v, positions in order.items()
         for p in positions]
  # print(v_p)
  return [x[0] for x in sorted(v_p, key=lambda v: v[1])]



class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.initial = []
    self.pos = []
    self.at = defaultdict(list)
    self.values = set()
    self.key = 1

  def reset(self):
    # for future use
    pass

  def pos_to_list(self, order):
    p_v = [(order[i], self.initial[i]) for i in range(len(order))]
    # print(p_v)
    return [x[1] for x in sorted(p_v, )]

  def do_line(self, line):
    # called for each line of input
    v = int(line)
    pos = len(self.initial)
    self.pos.append(pos)
    if v == 0:
     self.zero = pos
    self.initial.append(v)
    # self.at[v].append(len(self.initial) - 1)
    if v in self.values:
      # print("Duplicate", v)
      pass
    # assert v not in self.values
    self.values.add(v)

  def post_load(self):
    # called after all input is read
    self.size = len(self.initial)
    if self.size < 10:
      print(self.initial)
      #XXX print(self.at)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    b = list(self.pos)
    positions = list(self.pos)
    new_order = self.mix(positions)
    mixed = self.pos_to_list(new_order)
    print('mixed=', mixed[0:20])

    zero_pos = new_order[self.zero]
    print('zero moves from ', self.zero, 'to', zero_pos)
    assert mixed[zero_pos] == 0

    a = mixed[(zero_pos + 1000) % self.size]
    b = mixed[(zero_pos + 2000) % self.size]
    c = mixed[(zero_pos + 3000) % self.size]
    print('a b c', a, b, c)
    return a + b + c


  def mix(self, positions):
    for thing in range(self.size):
      v = self.initial[thing]
      pos = positions[thing]
      if v == 0:
        continue

      if v > 0:
        np = pos + v
        # Not quite
        #if np >= self.size:
        #  np += 1
        #n_pos = np % self.size
        n_pos = np % (self.size - 1)
      else:
        np = pos + v
        if np <= 0:
          np -= 1
        # n_pos = (pos + v - 1) % self.size
        n_pos = (pos + v) % (self.size - 1)

      # compute range to decrement or increment
      if pos < n_pos:
        disp = -1
        r_low = pos + 1
        r_high = n_pos
      else:
        disp = 1
        r_low = n_pos
        r_high = pos - 1
      if TRACE > 0:
        # print('')
        print('  move %3d' % v, 'from', pos, 'to', n_pos, ' adjust range:', r_low, r_high, disp)

      for pi, opos in enumerate(positions):
        if opos == pos:
          # print('    ', '%3d' % ov, 'from', opos, 'to', opos+disp)
          if TRACE > 1:
            print('    self to', n_pos)
          positions[pi] = n_pos
        elif opos >= r_low and opos <= r_high:
          positions[pi] = opos + disp
          ov = self.initial[pi]
          if TRACE > 2:
            print('    ', '%3d' % ov, 'from', opos, 'to', opos+disp)
      if TRACE > 0:
        # print('   >positions', positions)
        print('   >', self.pos_to_list(positions))

    return positions

  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.key = 811589153
    for i in range(self.size):
      self.initial[i] = self.initial[i] * 811589153


    positions = list(self.pos)
    for i in range(10):
      new_order = self.mix(positions)
      mixed = self.pos_to_list(new_order)
      print('mixed=', mixed[0:20])

    zero_pos = new_order[self.zero]
    print('zero moves from ', self.zero, 'to', zero_pos)
    assert mixed[zero_pos] == 0
    a = mixed[(zero_pos + 1000) % self.size]
    b = mixed[(zero_pos + 2000) % self.size]
    c = mixed[(zero_pos + 3000) % self.size]
    print('a b c', a, b, c)
    return a + b + c



day20.sample_test("""
1
2
-3
3
-2
0
4
""", expect1=3, expect2=1623178306)

TRACE=0

if __name__ == '__main__':
  # part1: not -9746, -5555, 9517
  day20.run_and_check('input.txt', expect1=18257, expect2=4148032160983)
