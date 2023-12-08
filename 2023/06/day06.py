#!/usr/bin/env python3
"AOC 2023: day 06"

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

  def do_line(self, line):
    # called for each line of input
    x = line.strip().split(' ')
    if x[0] == 'Time:':
      self.times = [int(t) for t in x[1:] if t]
      # print(self.times)
    elif x[0] == 'Distance:':
      self.distance = [int(d) for d in x[1:] if d]
    else:
      print(x)
      assert False

  def press_to_dist(self, t_press, max_time):
    moving_time = max_time - t_press
    dist = moving_time * t_press
    return dist

  def part1(self):
    print('===== Start part 1')
    ret = 1
    for race in range(len(self.times)):
      wins = 0
      race_t = self.times[race]
      race_d = self.distance[race]
      for t in range(1, race_t-1):
        dist = self.press_to_dist(t, race_t)
        if dist > race_d:
          wins += 1
      ret *= wins
    return ret

  def part2(self):
    print('===== Start part 2')
    self.reset()
    race_t = int(''.join(['%d' % x for x in self.times]))
    race_d = int(''.join(['%d' % x for x in self.distance]))
    print('part2 race:', race_t, race_d)

    # brute force
    min_s = race_d // race_t
    wins = 0
    for t in range(min_s, race_t-1):
      dist = self.press_to_dist(t, race_t)
      if dist > race_d:
        wins += 1
    print('part2', wins)
    return wins


day06.sample_test("""
Time:      7  15   30
Distance:  9  40  200
""", expect1=288, expect2=71503)


if __name__ == '__main__':
  day06.run_and_check('input.txt', expect1=505494, expect2=23632299)
