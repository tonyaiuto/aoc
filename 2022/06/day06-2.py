#!/usr/bin/env python3
"AOC 2021: day 06"

from tools import aoc


class day06(aoc.aoc):

  def __init__(self):
    super(day06, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def part1(self):
    print('===== Start part 1')
    data = self.all_input[0]
    return find_start(data, 4)

  def part2(self):
    print('===== Start part 2')
    data = self.all_input[0]
    return find_start(data, 14)

def find_start(s, sop_len):
  last = [-1] * 26
  start = 0
  for ci in range(len(s)):
    if ci == start + sop_len:
      return ci
    letter = ord(s[ci]) - ord('a')
    if last[letter] >= start:
      start = last[letter] + 1
    last[letter] = ci
  # This is probably rwon
  if len(s) == start + sop_len:
    return len(s)
  return -1


day06.sample_test("""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""", expect1=7, expect2=19)

day06.sample_test("""
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
""", expect1=11, expect2=26)


if __name__ == '__main__':
  day06.run_and_check('input.txt', expect1=1155, expect2=2789)
