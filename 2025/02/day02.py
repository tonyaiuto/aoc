#!/usr/bin/env python3
"AOC 2025: day 02"

from tools import aoc


def is_invalid1(i):
  s = str(i)
  ls = len(s)
  if ls % 2 == 1:
    return False
  if s[:ls//2] == s[ls//2:]:
    return True
  return False

def repeats_at_size(s, n):
  # print(f"check {s} at {n}")
  id = s[:n]
  for i in range(1, len(s) // n):
    # print("  ", id, s[n*i:n*i+n])
    if id != s[n*i:n*i+n]:
      return False
  return True


def is_invalid2(i):
  s = str(i)
  ls = len(s)
  for n in range(1, ls//2 + 1):
    # Can we divide evenly by this size?
    if ls % n == 0:
      if repeats_at_size(s, n):
        return True
  return False


class day02(aoc.aoc):

  def __init__(self):
    super(day02, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.ranges = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    for id_range in line.split(","):
      low, high = id_range.split("-")
      self.ranges.append((int(low), int(high)))

  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    for low, high in self.ranges:
       for i in range(low, high+1):
         if is_invalid1(i):
           print("Invalid", i)
           ret += i
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for low, high in self.ranges:
       for i in range(low, high+1):
         if is_invalid2(i):
           print("Invalid", i)
           ret += i
    return ret


day02.sample_test("""
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""", expect1=1227775554, expect2=4174379265)


if __name__ == '__main__':
  day02.run_and_check('input.txt', expect1=None, expect2=None)
