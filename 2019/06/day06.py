#!/usr/bin/env python3

from memoized import memoized

class Orbits(object):

  def __init__(self):
    self.orbits = {}
    self.dists = {}

  def from_file(self, path):
    with open(path, 'r') as inp:
      for line in inp:
        line = line.strip()
        if line:
          obj, orbiter = line.split(')')
          self.add_orbit(obj, orbiter)

  def from_string(self, s):
    for line in s.split('\n'):
      obj, orbiter = line.strip().split(')')
      self.add_orbit(obj, orbiter)

  def add_orbit(self, obj, orbiter):
    # print('%s -> %s' % (obj, orbiter))
    self.orbits[orbiter] = obj

  def total_orbits(self):
    ret = 0
    for obj in self.orbits.keys():
      ret += self.orb_dist(obj)
    return ret

  def orb_dist(self, obj):
    if obj == 'COM':
      return 0
    d = self.dists.get(obj)
    if not d:
      d = 1 + self.orb_dist(self.orbits[obj])
      self.dists[obj] = d
    return d

  def path_to(self, obj):
    if obj == 'COM':
      return ['COM']
    ret = self.path_to(self.orbits[obj])
    ret.append(obj)
    return ret

  def n_trans(self, a, b):
    p_a = self.path_to(a)
    p_b = self.path_to(b)
    l_a = len(p_a) - 1
    l_b = len(p_b) - 1
    print(p_a)
    print(p_b)
    for i in range(l_a):
      if p_a[i] != p_b[i]:
        return l_a - i + l_b - i
    assert False


TEST_1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""

def test1():
  o = Orbits()
  o.from_string(TEST_1)
  assert o.total_orbits() == 42

TEST_2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

def test2():
  o = Orbits()
  o.from_string(TEST_2)
  assert o.path_to('YOU') == ['COM', 'B', 'C', 'D', 'E', 'J', 'K', 'YOU']
  assert o.n_trans('YOU', 'SAN') == 4


def part1():
  o = Orbits()
  o.from_file('input_06.txt')
  print('part1:', o.total_orbits())


def part2():
  o = Orbits()
  o.from_file('input_06.txt')
  print('part2:', o.n_trans('YOU', 'SAN'))


if __name__ == '__main__':
  part1()
  part2()
