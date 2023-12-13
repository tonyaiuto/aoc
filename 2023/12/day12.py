#!/usr/bin/env python3
"AOC 2023: day 12"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import memoized

DEBUG = False

class Report(object):

  def __init__(self, s):
    # ?#?#?#?#?#?#?#? 1,3,1,6
    tmp = s.split()
    self.len = len(tmp[0])
    self.raw = tmp[0] + '@'  # sentinal so we can always look past end
    self.need = [int(x) for x in tmp[1].split(',')]
    lneed = len(self.need)
    self.all_need = list(self.need)
    for i in range(lneed - 2, -1, -1):
      self.all_need[i] = self.need[i] + self.all_need[i+1]
    # print(self.raw, self.need, self.all_need)

  def __str__(self):
    return str(self)

  def count_patterns(self):
    self.got = []
    pos = 0
    while self.raw[pos] == '.':
      pos += 1
    self.at = [-1] * len(self.need)
    ok = self.match_at_pos(pos, 0)
    if DEBUG:
      print('==', self.raw, '=>', len(self.got))
    return len(self.got)


  # @memoized.memoized
  def match_at_pos(self, pos, need_i):
    # Matched them all?
    if need_i >= len(self.need):
      self.got.append(self.at)
      if DEBUG:
        print('   ' * need_i, 'Got', self.at)
      return True

    need = self.need[need_i]
    if DEBUG:
       print('  ' * need_i, 'match attempt @', pos, 'for', need)
    if pos + self.all_need[need_i] > self.len:
      if DEBUG:
        print('  ' * need_i, '> Dead end. Maxed out')
      return False

    while pos + self.all_need[need_i] <= self.len:
      # skip leading white space
      while self.raw[pos] == '.':
        pos += 1
        if pos >= self.len:
          if DEBUG:
            print('  ' * need_i, '   ran out OK')
          return False

      if pos + self.all_need[need_i] > self.len:
        if DEBUG:
          print('  ' * need_i, "  ran out - total")
        return False

      # assert part1_decode('?.?.????????? 1,4,1') == 8

      # Gather a section which could be damaged
      have = 0
      leading_wild = 0
      had_hash = False
      for ic in range(self.len-pos):
        c = self.raw[pos+ic]
        if c in ('#', '?'):
          have += 1
          if c == '?':
            if not had_hash:
              leading_wild += 1
          else:
            had_has = True
        else:
          break
  
      if have < need:  # not enough
        if DEBUG:
          print('  ' * need_i, "  ran out short at", pos, "got", have, "of", need)
        return False

      # assert part1_decode('?.?.????????? 1,4,1') == 8

      nxt = self.raw[pos+need]
      if DEBUG:
        print('  ' * need_i, "  nxt is @", pos+need, "=", nxt)
      # Cases: need = 2
      # .###
      # print('  ' * need_i, "   @pos=", self.raw[pos])
      if self.raw[pos] == '#' and nxt == '#':
        # More than we can use
        return False

      # 0123456789 12345678
      # ????.######..#####.@ [1, 6, 5]

      if nxt != '#':
        # .##.
        # .##?.
        # .##?#
        #if nxt != '#':
        self.at[need_i] = pos
        if DEBUG:
          print('  ' * need_i, "  > recurse @", pos+need+1)
        ok = self.match_at_pos(pos+need+1, need_i+1)
        if DEBUG:
          print('  ' * need_i, "  < back from @", pos+need+1, ok)

        pos += 1
        if self.raw[pos] == '#':
          if ok:
            pos += need
          else:
            return False
      else:
        # .?..    <- reduce to '.'
        # .?#.
        # .??.
        # .??#
        # .???.
        # .???#
        # assert self.raw[pos] == '?'
        # imagine first is a '.'
        pos += 1

    if pos + self.all_need[need_i] > self.len:
      if DEBUG:
        print('  ' * need_i, '   ran out maxneed')
    return False


def part1_decode(s):
  rep = Report(s)
  if DEBUG:
    print('==== Check', rep.raw, rep.need)
  ret = rep.count_patterns()
  print('==== Check', rep.raw, rep.need, '->', ret)
  return ret


class day12(aoc.aoc):

  def __init__(self):
    super(day12, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.reports = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    rep = Report(line)
    self.reports.append(rep)

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    ret = 0
    for rep in self.reports:
      ret += rep.count_patterns()
    if ret >= 11559:
      print("part 1", ret, "TOO HIGH!")
    print("part 1", ret)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42

assert part1_decode('???.### 1,1,3') == 1
assert part1_decode('.??..??...?##. 1,1,3') == 4
assert part1_decode('?#?#?#?#?#?#?#? 1,3,1,6') == 1
assert part1_decode('????.#...#... 4,1,1') == 1
DEBUG = True
assert part1_decode('????.######..#####. 1,6,5') == 4
assert part1_decode('?###???????? 3,2,1') == 10
assert part1_decode('?.?.????????? 1,4,1') == 8
assert part1_decode('.??????????. 1,4,2') == 0

day12.sample_test("""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""", expect1=21, expect2=None)



if __name__ == '__main__':
  day12.run_and_check('input.txt', expect1=None, expect2=None)
