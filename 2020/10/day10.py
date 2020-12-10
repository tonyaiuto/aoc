"AOC 2020: day 10"

from collections import defaultdict
from tools import reader
from tools.memoized import memoized


def sample_test(s, expect):
  puzz = day10()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res
  puzz.part2()
  print('part2', puzz.result2)


def main(input):
  puzz = day10()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  res = puzz.part2()
  print('part2', res)


class day10(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.max_jolt = 0
    self.ratings = [0]
    pass

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.prep()

  def load_str(self, s):
    all = reader.StringReader(s).load()
    print(all)
    for x in all:
      self.do_line(x)
    self.prep()

  def do_line(self, line):
    if not line:
      return
    jolt = int(line)
    self.ratings.append(jolt)
    self.max_jolt = max(self.max_jolt, jolt)

  def prep(self):
    rating = self.max_jolt + 3
    self.ratings.sort()
    self.ratings.append(rating)
    print(self.ratings)
    self.diffs = [0]
    for i, v in enumerate(self.ratings):
      if i > 0:
        diff = v - self.ratings[i-1]
        assert diff <= 3
        self.diffs.append(diff)
    print(self.diffs)

  def part1(self):
    top_volt = 0
    # [1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]
    diff1 = 0
    diff3 = 0
    for i, v in enumerate(self.ratings):
      diff = v - top_volt
      top_volt = v
      if diff == 1:
        diff1 += 1
      if diff == 3:
        diff3 += 1
      # print('@', i, 'v', v, 'diff1,3', diff, diff1, diff3)
    self.result1 = diff1 * diff3
    return self.result1

  def part2(self):
    end_rating = self.max_jolt + 3
    good = 0

    """
    def try_next(i, top_volt):
      nonlocal good
      for j in range(i, len(self.ratings)):
        v = self.ratings[j]
        # print('top', top_volt, j, v)
        if top_volt + 3 >= v:
          if v == end_rating:
            # print("OK")
            good += 1
            return
          try_next(j+1, self.ratings[j]) 
        else:
          break
    try_next(0, 0)
    """

    self.result2 = self.paths_to_me(len(self.ratings)-1)
    return self.result2

  @memoized
  def paths_to_me(self, me):
    if me == 0:
      return 1
    n_paths = 0
    for j in range(3):
      back = me - 1 - j
      if back >= 0:
        if self.ratings[back] + 3 >= self.ratings[me]:
          n_paths += self.paths_to_me(back)
      #else:
      #  n_paths = 1
    print(n_paths, 'paths to', self.ratings[me], '@', me)
    return n_paths
 

   
  



sample_test("""
16
10
15
5
1
11
7
19
6
12
4
""", 35)

sample_test("""
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""", 220)

if __name__ == '__main__':
  main('input.txt')
  pass
