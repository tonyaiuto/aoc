#!/usr/bin/env python3
"AOC 2021: day 13"

import json

from tools import aoc

def v_comp(l, r):
  if not l:
    if isinstance(r, list) and r:
      return -1
    return 0
  if not r:
    if isinstance(l, list) and l:
      return 1
    return 0

  lv = l[0]
  rv = r[0]
  if isinstance(lv, int):
    if isinstance(rv, int):
      if lv < rv:
        return -1
      if lv > rv:
        return 1
    else:
      # l int, r list
      lv = [lv]
      ret = v_comp(lv, rv)
      if ret != 0:
        return ret
    return v_comp(l[1:], r[1:])

  assert isinstance(lv, list)
  if isinstance(rv, int):
    rv = [rv]
    ret = v_comp(lv, rv)
    if ret != 0:
      return ret
  else:
    assert isinstance(rv, list)
    ret = v_comp(lv, rv)
    if ret != 0:
      return ret
  return v_comp(l[1:], r[1:])


class Packet(object):

  def __init__(self, s):
    self.p = json.loads(s)

  def __str__(self):
    return str(self.p)

  def compare(self, o):
    cmp = v_comp(self.p, o.p)
    if cmp < 0:
      return True
    if cmp > 0:
      return False
    print("EQUAL?", self, o)
    return True

  def __lt__(self, o):
    cmp = v_comp(self.p, o.p)
    return cmp < 0

  def __eq__(self, o):
    cmp = v_comp(self.p, o.p)
    return cmp == 0


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.pair_index = 0
    self.ret1 = 0
    self.packets = []

  def do_line(self, line):
    self.pair_index += 1
    # called for each line of input
    a = Packet(line[0])
    self.packets.append(a)
    b = Packet(line[1])
    self.packets.append(b)
    is_ok = a.compare(b)
    # print(a, b, self.pair_index, is_ok)
    if is_ok:
      self.ret1 += self.pair_index

  def post_load(self):
    # called after all input is read
    pass

  def part1(self):
    print('===== Start part 1')
    return self.ret1

  def part2(self):
    print('===== Start part 2')
    self.packets.append(Packet("[[2]]"))
    self.packets.append(Packet("[[6]]"))

    foo = sorted(self.packets)
    i = 0
    ret = 0
    for p in foo:
      i += 1
      if str(p) == '[[2]]':
        ret = i
      if str(p) == '[[6]]':
        ret *= i
        break

    return ret


day13.sample_test("""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""", expect1=13, expect2=140)


if __name__ == '__main__':
  day13.run_and_check('input.txt', expect1=4894, expect2=24180)
