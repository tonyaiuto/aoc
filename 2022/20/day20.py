#!/usr/bin/env python3
"AOC 2021: day 20"

from collections import defaultdict
import copy
import itertools

from tools import aoc



def order_to_list(order):
  v_p = [(v, p)
         for v, positions in order.items()
         for p in positions]
  print(v_p)
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

  def reset(self):
    # for future use
    pass

  def pos_to_list(self, order):
    p_v = [(p, self.initial[p]) for p in order]
    return [x[1] for x in sorted(p_v)]

  def do_line(self, line):
    # called for each line of input
    v = int(line)
    self.pos.append(len(self.initial))
    self.initial.append(v)

    self.at[v].append(len(self.initial) - 1)
    if v in self.values:
      print("Duplicate", v)
    assert v not in self.values
    self.values.add(v)

  def post_load(self):
    # called after all input is read
    print(self.initial)
    print(self.at)
    self.size = len(self.initial)

  def part1(self):
    print('===== Start part 1')
    self.reset()
    b = list(self.initial)
    order = self.mix(b)
    print('new order', self.pos_to_list(order))
    # plist = sorted([(pos, v) for v, pos in order.items()])
    # res = [v[1] for v in plist]
    print('final', res)

    zero_pos = order[0]
    print('zero at', zero_pos)
    a = res[(zero_pos + 1000) % self.size]
    b = res[(zero_pos + 2000) % self.size]
    c = res[(zero_pos + 3000) % self.size]
    print('a b c', a, b, c)
    return a + b + c

    """
Then, the grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers after the value 0, wrapping around the list as necessary. In the above example, the 1000th number after 0 is 4, the 2000th is -3, and the 3000th is 2; adding these together produces 3.
"""

  def mix(self, b):
    order = dict(self.at)

    print('order', order)
    positions = list(self.pos)
    for thing in range(self.size):
      v = self.initial[thing]
      pos = positions[thing]
      if v == 0:
        continue

      if v > 0:
        np = pos + v
        if np >= self.size:
          np += 1
        n_pos = np % self.size
      else:
        #if pos + v == 0:
        # we should be at the end
        n_pos = (pos + v - 1) % self.size
      print('')
      print('  move %3d' % v, 'from', pos, 'to', n_pos)

      # compute range to decrement or increment
      if pos < n_pos:
        disp = -1
        r_low = pos + 1
        r_high = n_pos
      else:
        disp = 1
        r_low = n_pos + 1
        r_high = pos

      for pi, opos in enumerate(positions):
        if opos == pos:
          # print('    ', '%3d' % ov, 'from', opos, 'to', opos+disp)
          print('    self to', n_pos)
          positions[pi] = n_pos
        if opos >= r_low and opos <= r_high:
          positions[pi] = opos + disp
          ov = self.initial[pi]
          print('    ', '%3d' % ov, 'from', opos, 'to', opos+disp)

      """
      # print("  adjust range:", r_low, r_high, disp)
      for ov, opositions in order.items():
        order[ov] = []
        for opos in opositions:
          if ov == v and pos == opos:
            # print("DO NOT MOVE SELF")
            order[ov].append(n_pos)
            continue
          if opos >= r_low and opos <= r_high:
            order[ov].append(opos + disp)
            print('    ', '%3d' % ov, 'from', opos, 'to', opos+disp)
      print(order_to_list(order))
      """
    return positions

  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day20.sample_test("""
1
2
-3
3
-2
0
4
""", expect1=3, expect2=None)


if __name__ == '__main__':
  day20.run_and_check('input.txt', expect1=None, expect2=None)
