#!/usr/bin/env python3

from functools import reduce
from math import gcd

"""
--- Day 12: The N-Body Problem ---
The space near Jupiter is not a very safe place; you need to be
careful of a big distracting red spot, extreme radiation, and a
whole lot of moons swirling around. You decide to start by tracking
the four largest moons: Io, Europa, Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon (your
puzzle input). You just need to simulate their motion so you can
avoid them.
"""

class Body(object):

  def __init__(self, x, y, z):
    # Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional
    # velocity. The position of each moon is given in your scan; the x,
    # y, and z velocity of each moon starts at 0.
    self.x = x
    self.y = y
    self.z = z
    self.vx = 0
    self.vy = 0
    self.vz = 0

  def __str__(self):
     return 'pos=<x=%3d, y=%3d, z=%3d>, vel=<x=%3d, y=%3d, z=%3d>' % (
         self.x, self.y, self.z, self.vx, self.vy, self.vz)

  def __eq__(self, other):
      return (self.x == other.x
              and self.y == other.y
              and self.z == other.z
              and self.vx == other.vx
              and self.vy == other.vy
              and self.vz == other.vz)


class System(object):

  def __init__(self, bodies):
    self.bodies = bodies
    self.time = 0


  def __str__(self):
    return '\n'.join([str(b) for b in self.bodies])

  def x_dims(self):
    return [(b.x, b.vx) for b in self.bodies]

  def y_dims(self):
    return [(b.y, b.vy) for b in self.bodies]

  def z_dims(self):
    return [(b.z, b.vz) for b in self.bodies]

  def time_step(self):
    # Simulate the motion of the moons in time steps. Within each time
    # step, first update the velocity of every moon by applying gravity.
    # Then, once all moons' velocities have been updated, update the
    # position of every moon by applying velocity. Time progresses by one
    # step once all of the positions are updated.
    self.do_timestep_x()
    self.do_timestep_y()
    self.do_timestep_z()
    self.time += 1


  def do_timestep_x(self):
    # To apply gravity, consider every pair of moons. On each axis (x,
    # y, and z), the velocity of each moon changes by exactly +1 or -1
    # to pull the moons together. For example, if Ganymede has an x
    # position of 3, and Callisto has a x position of 5, then Ganymede's
    # x velocity changes by +1 (because 5 > 3) and Callisto's x velocity
    # changes by -1 (because 3 < 5). However, if the positions on a given
    # axis are the same, the velocity on that axis does not change for
    # that pair of moons.

    # Once all gravity has been applied, apply velocity: simply add the
    # velocity of each moon to its own position. For example, if Europa
    # has a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3,
    # then its new position would be x=-1, y=2, z=6. This process does
    # not modify the velocity of any moon.

    tmp = sorted(self.bodies, key=lambda body: body.x)
    for near_i, near in enumerate(self.bodies):
      for _, far in enumerate(self.bodies, start=near_i+1):
        if near.x < far.x:
          near.vx += 1
          far.vx -= 1
    for b in self.bodies:
      b.x += b.vx

  def do_timestep_y(self):
    tmp = sorted(self.bodies, key=lambda body: body.y)
    for near_i, near in enumerate(self.bodies):
      for _, far in enumerate(self.bodies, start=near_i+1):
        if near.y < far.y:
          near.vy += 1
          far.vy -= 1
    for b in self.bodies:
      b.y += b.vy

  def do_timestep_z(self):
    tmp = sorted(self.bodies, key=lambda body: body.z)
    for near_i, near in enumerate(self.bodies):
      for _, far in enumerate(self.bodies, start=near_i+1):
        if near.z < far.z:
          near.vz += 1
          far.vz -= 1
    for b in self.bodies:
      b.z += b.vz


  def energy(self):
    # Then, it might help to calculate the total energy in the system.
    # The total energy for a single moon is its potential energy multiplied
    # by its kinetic energy. A moon's potential energy is the sum of the
    # absolute values of its x, y, and z position coordinates. A moon's
    # kinetic energy is the sum of the absolute values of its velocity
    # coordinates. Below, each line shows the calculations for a moon's
    # potential energy (pot), kinetic energy (kin), and total energy:
    e = 0
    for b in self.bodies:
      e += (abs(b.x) + abs(b.y) + abs(b.z)) * (abs(b.vx) + abs(b.vy) + abs(b.vz))
    return e

def prep_1():
  return  System([
      Body(x=-1, y=0, z=2),
      Body(x=2, y=-10, z=-7),
      Body(x=4, y=-8, z=8),
      Body(x=3, y=5, z=-1),
      ]) 

EXPECT_1 = [
    'pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>',
    'pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>',
    'pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>',
    'pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>',
    ]


def test_body_eq():
  a = Body(x=3, y=5, z=-1)
  b = Body(x=3, y=5, z=-1)
  assert a == b


def test_system_1():
  j = prep_1()
  for i in range(10):
    j.time_step()
    # print(str(j))

  for i, expect in enumerate(EXPECT_1):
    if expect.replace(' ', '') != str(j.bodies[i]).replace(' ', ''):
      msg = 'FAIL: %d, expected %s, got %s' % (i, expect, str(j.bodies[i]))
      print(msg)
      raise Exception(msg)
  assert j.energy() == 179
  print('PASS: test_system_1')

def test_system_axis():
  j = prep_1()
  for i in range(10):
    j.do_timestep_x()
    j.do_timestep_y()
    j.do_timestep_z()

  for i, expect in enumerate(EXPECT_1):
    if expect.replace(' ', '') != str(j.bodies[i]).replace(' ', ''):
      msg = 'FAIL: %d, expected %s, got %s' % (i, expect, str(j.bodies[i]))
      print(msg)
      raise Exception(msg)
  assert j.energy() == 179
  print('PASS: test_system_axis')


def prep_2():
  return System([
      Body(x=-8, y=-10, z=0),
      Body(x=5, y=5, z=10),
      Body(x=2, y=-7, z=3),
      Body(x=9, y=-8, z=-3),
      ])

def test_system_2():
  j = prep_2()
  for i in range(100):
    j.time_step()

  expected = [
      'pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>',
      'pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>',
      'pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>',
      'pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>',
  ]
  for i, expect in enumerate(expected):
    if expect.replace(' ', '') != str(j.bodies[i]).replace(' ', ''):
      msg = 'FAIL: %d, expected %s, got %s' % (i, expect, str(j.bodies[i]))
      print(msg)
      raise Exception(msg)
  assert j.energy() == 1940
  print('PASS: test_system_2')
  """
  Energy after 100 steps:
  pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
  pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
  pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
  pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
  Sum of total energy: 290 + 608 + 574 + 468 = 1940
  """


test_body_eq()
test_system_1()
test_system_axis()
test_system_2()

def part1():
  # What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
  io = Body(x=0, y=6, z=1)
  europa = Body(x=4, y=4, z=19)
  ganymede = Body(x=-11, y=1, z=8)
  callisto = Body(x=2, y=19, z=15)
  jupiter = System([io, europa, ganymede, callisto])
  for i in range(1000):
    jupiter.time_step()
  print('part1:', jupiter.energy())

part1()

def find_period(system):
  original = System([Body(b.x, b.y, b.z) for b in system.bodies])
  original_x_dims = original.x_dims()
  original_y_dims = original.y_dims()
  original_z_dims = original.z_dims()

  x_period = 0
  while True:
    system.do_timestep_x()
    x_period += 1
    if original_x_dims == system.x_dims():
      break
  print('x_period:', x_period)

  y_period = 0
  while True:
    system.do_timestep_y()
    y_period += 1
    if original_y_dims == system.y_dims():
      break
  print('y_period:', y_period)

  z_period = 0
  while True:
    system.do_timestep_z()
    z_period += 1
    if original_z_dims == system.z_dims():
      break
  print('z_period:', z_period)
  periods = [x_period, y_period, z_period]
  lcm = periods[0]
  for i in periods[1:]:
    lcm = lcm * i // gcd(lcm, i)
  return lcm


def test_period():
  j = prep_1()
  period = find_period(j)
  assert 2772 == period
  print('PASS: test_system_axis')

  j = prep_2()
  period = find_period(j)
  print('test2: period', period)
  # assert 4686774924 == period
  print('PASS: test_system_axis')


test_period()

def part2():
  io = Body(x=0, y=6, z=1)
  europa = Body(x=4, y=4, z=19)
  ganymede = Body(x=-11, y=1, z=8)
  callisto = Body(x=2, y=19, z=15)
  jupiter = System([io, europa, ganymede, callisto])
  period = find_period(jupiter)
  assert 282270365571288 == period
  print('part2: period=%d' % period)

part2()
