#!/usr/bin/env python3
"AOC 2025: day 01"

from tools import aoc


class day01(aoc.aoc):

  def __init__(self):
    super(day01, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.pos = 50
    self.dir = []
    self.moves = []
    self.moves2 = []

  def reset(self):
    # for future use
    self.pos = 50
    pass

  def do_line(self, line):
    if not line:
      return
    dir = line[0]
    self.dir.append(dir)
    move = int(line[1:])
    revs = move // 100
    left = move % 100
    if dir == 'L':
       move = 100 - move
       left = -left
    self.moves.append(move)
    self.moves2.append((dir, revs, left))

  def part1(self):
    print('===== Start part 1')
    self.reset()

    ret = 0
    for move in self.moves:
      self.pos = (self.pos + move) % 100
      if self.pos == 0:
        ret += 1
    return ret


  def part2(self):
    print('===== Start part 2')
    self.reset()
    ret = 0
    for mv in self.moves2:
      dir = mv[0]
      revs = mv[1]
      move = mv[2]

      orig = self.pos
      ret += revs
      self.pos += move

      if self.pos == 0:
        # print("Land on 0")
        ret += 1
      elif self.pos < 0: 
        if orig > 0:
          # print("crossed 0")
          ret += 1
        self.pos += 100
      elif self.pos >= 100:
        ret += 1
        self.pos = self.pos % 100
      # print(orig, 'x', dir, revs, move, '->', self.pos, ret)
    return ret


day01.sample_test("""
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""", expect1=3, expect2=6)

# not 6125

if __name__ == '__main__':
  day01.run_and_check('input.txt', expect1=1147, expect2=6789)
