#!/usr/bin/env python3
"AOC 2023: day 19"

from collections import defaultdict
import itertools
import sys

from tools import aoc


class day19(aoc.aoc):

  def __init__(self):
    super(day19, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.patterns = []
    self.by_first = defaultdict(list)
    self.towels = []

  def do_line(self, line):
    # called for each line of input
    if not self.patterns:
      for p in line.split(','):
        pat = p.strip()
        self.patterns.append(pat)
        self.by_first[pat[0]].append(pat)
    else:
      if line:
        self.towels.append(line)

  def post_load(self):
    # called after all input is read
    self.towels = sorted(self.towels, key=lambda x: len(x))
    # Make the by_first lists sorted from longest down.
    self.by_first = {k: sorted(v, key=lambda x: len(x), reverse=True)
                     for k, v in self.by_first.items()}
    if self.doing_sample:
      print(self.patterns)
      print(self.by_first)
 

  def part1(self):
    print('===== Start part 1')
    ret = 0
    for towel in self.towels:
      if self.doing_sample:
        print("= Towel", towel)
      if self.can_do(towel):
        ret += 1
    return ret


  def can_do(self, towel):
    for pattern in self.by_first.get(towel[0], []):
      lp = len(pattern)
      if lp > len(towel):
        continue
      if pattern != towel[:lp]:
        continue

      if lp == len(towel):
        return True
      #if self.doing_sample:
      #  print(towel, "munched", pattern, "trying", towel[lp:])
      if self.can_do(towel[lp:]):
        return True
    return False

  def part2(self):
    print('===== Start part 2')

    self.pattern_ways = None
    pattern_ways = {}
    for pattern in self.patterns:
      can = self.can_do2(pattern, defaultdict(int))
      assert can >= 1
      pattern_ways[pattern] = can
    self.pattern_ways = pattern_ways
    print(self.pattern_ways)

    ret = 0
    for towel in self.towels:
      print("= Towel", towel)
      if not self.can_do(towel):
        continue
      local_memo = defaultdict(int)
      can = self.can_do2(towel, local_memo)
      if can > 0:
        print("  > towel", can)
        ret += can
      if ret > 500:
        break
    return ret

  def can_do2(self, towel, local_memo, depth=0):
    ret = 0
    for pattern in self.by_first.get(towel[0], []):
      lp = len(pattern)
      if lp > len(towel):
        continue
      if pattern != towel[:lp]:
        continue

      ways = 1
      if self.pattern_ways:
        ways = self.pattern_ways[pattern]

      if lp == len(towel):
        ret += ways
        if self.pattern_ways:
           return ret
           break

      else:
        rest = towel[lp:]
        if rest in local_memo:
          ret += local_memo[rest] * ways
        else:
          if towel == 'grwbgrbbbwu' or self.doing_sample:
            print(' '*depth, '%-10s' % towel, "  munched", pattern, "trying", towel[lp:], "ways", ways)
          more = self.can_do2(rest, local_memo, depth=depth+1)
          if towel == 'grwbgrbbbwu' or self.doing_sample:
            print(' '*depth, "            got", more)
          if more > 0:
            # ret += more * ways
            ret += more * 1
            local_memo[rest] += ret

    return ret


day19.sample_test("""
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""", expect1=6, expect2=16)


if __name__ == '__main__':
  # part 2: 346249370680  too low
  #         5448505536
  #         89264946828480 still too low
  day19.run_and_check('input.txt', expect1=263, expect2=None)
