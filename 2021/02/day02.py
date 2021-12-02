"AOC 2021: day 02"

from collections import defaultdict
import math

from tools import aoc


class day02(aoc.aoc):

  def __init__(self):
    super(day02, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
        })
    self.trace = True
    self.x = 0
    self.depth = 0
    self.aim = 0
    self.cmds = []

  def do_line(self, line):
    # called for each line of input
    self.cmds.append(line.split(' '))
    pass

  def part1(self):
    print('===== Start part 1')
    self.reset()
    for x in self.cmds:
      verb = x[0]
      dist = int(x[1])
      if verb == 'forward':
        self.x += dist
      elif verb == 'up':
        self.depth += dist
      elif verb == 'down':
        self.depth -= dist
      else:
        raise Exception("WTF: " + x)

    return self.x * -self.depth


  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.result2 = None
    for x in self.cmds:
      verb = x[0]
      dist = int(x[1])
      if verb == 'forward':
        self.x += dist
        self.depth += self.aim * dist
      elif verb == 'up':
        self.aim -= dist
      elif verb == 'down':
        self.aim += dist
      else:
        raise Exception("WTF: " + x)

    return self.x * self.depth


day02.sample_test("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
""", expect1=150, expect2=900)


if __name__ == '__main__':
  day02.run_and_check('input.txt', expect1=1989265, expect2=2089174012)
