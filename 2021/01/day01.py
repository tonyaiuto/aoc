"AOC 2021: day 01"

from collections import defaultdict
import math

from tools import aoc


class day01(aoc.aoc):

  def __init__(self):
    super(day01, self).__init__()
    self.n = []

  def do_line(self, line):
    self.n.append(int(line))

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.result1 = None
    inc = 0
    last = self.n[0]
    for val in self.n[1:]:
      if val > last:
        inc += 1
      last = val
    self.result1 = inc
    return self.result1


  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = None

    inc = 0
    last = sum(self.n[0:3])
    for val in window3(self.n):
      if val > last:
        inc += 1
      last = val
    self.result2 = inc
    return self.result2


def window3(v):
  win = v[0] + v[1] + v[2]
  for i in range(len(v)-3):
    yield win
    win = win - v[i] + v[i+3]
  yield win


day01.sample_test("""
199
200
208
210
200
207
240
269
260
263
""", expect1=7, expect2=5)


if __name__ == '__main__':
  day01.run_and_check('input.txt', expect1=1139, expect2=1103)
