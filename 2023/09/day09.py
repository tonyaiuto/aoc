#!/usr/bin/env python3
"AOC 2023: day 09"

from tools import aoc


class day09(aoc.aoc):

  def __init__(self):
    super(day09, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.values = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    hist = [int(x) for x in line.split(' ')]
    self.values.append(hist)
    pass

  def post_load(self):
    # called after all input is read
    pass


  def part1(self):
    print('===== Start part 1')
    sum = 0
    for seq in self.values:
      print('======', seq)
      nxt = find_next(seq)
      print(nxt, seq)
      sum += nxt

    return sum



  def part2(self):
    print('===== Start part 2')
    sum = 0
    for seq in self.values:
      print('======', seq)
      nxt = find_prev(seq)
      print(nxt, seq)
      sum += nxt
    return sum



def find_next(values):
   diff, all_zero = gen_dif(values)
   print('     ', diff)
   if all_zero:
      return values[-1]
   x = find_next(diff)
   return x + values[-1]

def find_prev(values):
   diff, all_zero = gen_dif(values)
   print('     ', diff)
   if all_zero:
      return values[0]
   x = find_prev(diff)
   return values[0] - x



def gen_dif(v):
  s = v[0]
  all_zero = True
  ret = []
  for v in v[1:]:
    d = v - s
    s = v
    if d != 0:
      all_zero = False
    ret.append(d)
  return ret, all_zero


day09.sample_test("""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""", expect1=114, expect2=2)


if __name__ == '__main__':
  day09.run_and_check('input.txt', expect1=1681758908, expect2=803)
