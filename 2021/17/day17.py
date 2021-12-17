#!/usr/bin/env python3
"AOC 2021: day 17"

from tools import aoc


NOTHING = 0
HIT = 3
OVERSHOOT = 1
UNDERSHOOT = 2

class Probe(object):

  def __init__(self, vx, vy):
    self.x = 0
    self.y = 0
    self.v_x = vx 
    self.v_y = vy

  def __str__(self):
    return 'probe: @%d,%d v:%d,%d' % (self.x, self.y, self.v_x, self.v_y)

  def step(self):
    self.x += self.v_x
    self.y += self.v_y
    if self.v_x > 0:
      self.v_x -= 1
    self.v_y -= 1


class day17(aoc.aoc):

  def __init__(self):
    super(day17, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def post_load(self):
    # called after all input is read

    self.trench = {}
    line = self.all_input[0]
    x, y = line[12:].split(',')
    _, r = x.split('=')
    i = r.find('..')
    self.trench_x_min = int(r[0:i])
    self.trench_x_max = int(r[i+2:])
    _, r = y.split('=')
    i = r.find('..')
    self.trench_y_min = int(r[0:i])
    self.trench_y_max = int(r[i+2:])
    if self.trench_y_max < self.trench_y_min:
      tmp = self.trench_y_min
      self.trench_y_min = self.trench_y_max
      self.trench_y_max = tmp

    for x in range(self.trench_x_min, self.trench_x_max+1):
      for y in range(self.trench_y_min, self.trench_y_max+1):
        self.trench[(x,y)] = 1 
 

  def step(self, probe):
    probe.step()
    # print(probe)
    if (probe.x, probe.y) in self.trench:
      return HIT
    if probe.x > self.trench_x_max:
      # print('Overshot at', probe)
      return OVERSHOOT
    if probe.y < self.trench_y_min:
      # print('Under glug at', probe)
      return UNDERSHOOT
    return 0

  def part1(self):
    print('===== Start part 1')

    vx_start = 0
    for vx in range(1, self.trench_x_max):
      probe = Probe(vx, 0)

      for i in range(100):
        e = self.step(probe)
        if e == HIT or e == OVERSHOOT:
          print('HIT? initial vx, probe', vx, probe)
          vx_start = vx
          break
      if vx_start:
        break

    ret = 0
    ret2 = 0
    for vx in range(vx_start-1, self.trench_x_max+1):
      for vy in range(self.trench_y_min, 100):
        probe = Probe(vx, vy)
        if self.trace_sample:
          print('Trying new probe', probe)
        max_y = 0
        for i in range(200):
          e = self.step(probe)
          max_y = max(max_y, probe.y)
          if e == HIT:
            if self.trace_sample:
              print('HIT for v:%d,%d, max:%d' % (vx, vy, max_y))
            ret = max(ret, max_y)
            ret2 += 1   
          if e != 0:
            break

    self.res2 = ret2
    return ret


  def part2(self):
    print('===== Start part 2')
    self.part1()
    return self.res2


day17.sample_test("""
target area: x=20..30, y=-10..-5
""", expect1=45, expect2=112)


if __name__ == '__main__':
  day17.run_and_check('input.txt', expect1=4278, expect2=1994)
