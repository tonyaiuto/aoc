#!/usr/bin/env python3
"AOC 2023: day 03"

import re

from tools import aoc

MUL_RE=re.compile(r"""mul\((\d+),(\d+)\)""")
DO_RE=re.compile(r"""do\(\)""")
DONT_RE=re.compile(r"""don't\(\)""")

class day03(aoc.aoc):

  def __init__(self):
    super(day03, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for inp in self.all_input:
      at = 0
      while True:
        # print(inp[at:])
        m = MUL_RE.search(inp, at)
        if not m:
          break
        # print(m.group(0))
        p = int(m.group(1)) * int(m.group(2))
        ret += p
        at = m.end()
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    enabled = True
    for inp in self.all_input:
      at = 0
      while at < len(inp):
        # print(inp[at:])
        m = MUL_RE.match(inp, at)
        if m:
          # print(m.group(0))
          if enabled:
            p = int(m.group(1)) * int(m.group(2))
            ret += p
          at = m.end()
          continue
        m = DO_RE.match(inp, at)
        if m:
          enabled = True
          at = m.end()
          continue
        m = DONT_RE.match(inp, at)
        if m:
          enabled = False
          at = m.end()
          continue

        at += 1
    return ret



day03.sample_test("""
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""", expect1=161, expect2=None)

day03.sample_test("""
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""", expect1=None, expect2=48)

if __name__ == '__main__':
  # low 28546082
  day03.run_and_check('input.txt', expect1=173517243, expect2=100450138)
