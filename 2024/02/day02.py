#!/usr/bin/env python3
"AOC 2023: day 02"

from tools import aoc

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
    self.rows = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    self.rows.append([int(x) for x in line.split(' ')])

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    n_safe = 0
    for row in self.rows:
      if is_safe(row):
        n_safe += 1
    return n_safe


  def part2(self):
    print('===== Start part 2')
    self.reset()
    n_safe = 0
    for row in self.rows:
      if is_safe(row):
        n_safe += 1
        continue
      # some days you just brute force it.
      for i in range(len(row)):
        xrow = row[0:i] + row[i+1:]
        # print(row, '->', xrow)
        if is_safe(xrow):
          n_safe += 1
          break
    return n_safe

def is_safe(values):
  vv = values
  if values[0] > values[-1]:
    vv = values[::-1]
  lv = vv[0]
  for v in vv[1:]:
    d = v - lv
    if d < 1 or d > 3:
      return False
    lv = v
  return True


day02.sample_test("""
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""", expect1=2, expect2=4)


if __name__ == '__main__':
  day02.run_and_check('input.txt', expect1=369, expect2=428)
  pass
