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
    self.id_sum = 0
    self.ps_sum = 0

  def do_line(self, line):
    # called for each line of input
    x = line.strip().split(':')
    game = x[0].strip().split(' ')
    id = int(game[1])
    possible = True
    sets = []
    max_r = 0
    max_g = 0
    max_b = 0
    for s in x[1].strip().split(';'):
       r = 0
       g = 0
       b = 0
       for x in s.strip().split(','):
         cubes = x.strip().split(' ')
         if cubes[1] == 'red':
           r = int(cubes[0])
           if r > 12:
             possible = False
         if cubes[1] == 'green':
           g = int(cubes[0])
           if g > 13:
             possible = False
         if cubes[1] == 'blue':
           b = int(cubes[0])
           if b > 14:
             possible = False
       sets.append([r, g, b])
       max_r = max(max_r, r)
       max_g = max(max_g, g)
       max_b = max(max_b, b)
    ps = max_r * max_g * max_b
    print("g", possible, ps, id, sets)
    if possible:
      self.id_sum += id
    self.ps_sum += ps

  def part1(self):
    print('===== Start part 1')
    self.reset()
    return self.id_sum


  def part2(self):
    print('===== Start part 2')
    self.reset()
    return self.ps_sum


day02.sample_test("""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""", expect1=8, expect2=None)


if __name__ == '__main__':
  day02.run_and_check('input.txt', expect1=2237, expect2=66681)
