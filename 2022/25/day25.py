#e!/usr/bin/env python3
"AOC 2021: day 25"

import sys

from tools import aoc

S_DIGIT_TO_INT = { '=': -2, '-': -1, '0': 0, '1': 1, '2': 2}

def from_snafu(s):
  ret = 0
  for c in s:
    d = S_DIGIT_TO_INT[c]
    ret = ret * 5 + d
  return ret

SAMPLES=[
      (        1, "1"),
      (        2, "2"),
      (        3, "1="),
      (        4, "1-"),
      (        5, "10"),
      (        6, "11"),
      (        7, "12"),
      (        8, "2="),
      (        9, "2-"),
      (       10, "20"),
      (       15, "1=0"),
      (       20, "1-0"),
      (     2022, "1=11-2"),
      (    12345, "1-0---0"),
      (314159265, "1121-1110-1=0"),
      (     4890, "2=-1=0"),
    ]

def test_from_snafu():
  for t in SAMPLES:
    v = from_snafu(t[1])
    if v != t[0]:
      print("fail on", t[1], 'got', v, 'expected', t[0])
      sys.exit(1)

def test_to_snafu():
  for t in SAMPLES:
    s = to_snafu(t[0])
    if s != t[1]:
      print("fail on", t[0], 'got', s, 'expected', t[1])
      sys.exit(1)


D_2_S = ['0', '1', '2', '=', '-', '0', '1', '2', '=', '-']
D_2_S = ['0', '1', '2', '=', '-', '0', '1', '2', '=', '-']

def to_snafu(v):
  ov = v
  ret = []
  while v > 0:
      last_digit = v % 10
      sd = D_2_S[last_digit]
      ret.append(sd)
  
      if last_digit >= 3:
        v += 5
      if last_digit >= 8:
        v += 5
      v -= last_digit
      v = v // 5
  return ''.join(reversed(ret))


test_to_snafu()
  


class day25(aoc.aoc):

  def __init__(self):
    super(day25, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.req = []

  def do_line(self, line):
    # called for each line of input
    self.req.append(from_snafu(line))

  def part1(self):
    print('===== Start part 1')
    s = sum(self.req)
    return to_snafu(s)


  def part2(self):
    return 42


day25.sample_test("""
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""", expect1='2=-1=0', expect2=None)


if __name__ == '__main__':
  day25.run_and_check('input.txt', expect1="2-0==21--=0==2201==2", expect2=None)
