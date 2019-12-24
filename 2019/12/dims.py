#!/usr/bin/env python3



class Dim(object):

  def __init__(self, values):
    self.initial = []
    self.bodies = []
    for v in values:
      self.initial.append([v, 0])
      self.bodies.append([v, 0])
    self.time = 0

  def time_step(self):
    tmp = sorted(self.bodies, key=lambda body: body[0])
    for near_i, near in enumerate(self.bodies):
      for _, far in enumerate(self.bodies, start=near_i+1):
        if near[0] < far[0]:
          near[1] += 1
          far[1] -= 1


def test2_dim():
  x = Dim([-1, 2, 4, 3])
  y = Dim([0, 10, -8, -7])
  z = Dim([2, -7, 8, -1])
  for i in range(10):
    x.time_step()
    y.time_step()
    z.time_step()
    
  expected = [
      'pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>',
      'pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>',
      'pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>',
      'pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>',
  ]
  for i, expect in enumerate(expected):
    got = 'pos=<x=%d,y=%d,z=%d>,vel=<x=%d,y=%d,z=%d>' % (
        x.bodies[i][0], y.bodies[i][0], z.bodies[i][0], x.bodies[i][1], y.bodies[i][1], z.bodies[i][1])
    if expect.replace(' ', '') != got:
      msg = 'FAIL: %d, expected %s, got %s' % (i, expect, got)
      print(msg)
      raise Exception(msg)
  # assert j.energy() == 179
