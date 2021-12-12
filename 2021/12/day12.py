#!/usr/bin/env python3
"AOC 2021: day 12"

from collections import defaultdict

from tools import aoc


class Cave(object):

  def __init__(self, name):
    self.name = name
    self.small = name.islower()
    self.edges = set()

  def __str__(self):
    return self.name

  def add_edge(self, cave):
    self.edges.add(cave)


class day12(aoc.aoc):

  def __init__(self):
    super(day12, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.caves = {}

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    c1, c2 = line.split('-')
    a = self.caves.get(c1) or Cave(c1)
    b = self.caves.get(c2) or Cave(c2)
    self.caves[a.name] = a
    self.caves[b.name] = b
    a.add_edge(b)
    b.add_edge(a)

  def post_load(self):
    # called after all input is read
    if self.trace_sample:
      print('start run: cave list')
      for cave in self.caves.values():
        print(cave.name, len(cave.edges), 'edges = ', ','.join([c.name for c in cave.edges]))

  def part1(self):
    print('===== Start part 1')
    self.reset()

    start = self.caves['start']
    visited = set()
    self.n_paths = 0
    self.walk(start, visited, 0)
    return self.n_paths

  def walk(self, s, visited, depth):
    # print('  ' * depth, s.name)
    depth += 1
    visited.add(s)
    for cave in s.edges:
       if cave.small and cave in visited:
         continue
       if cave.name == 'end':
         self.n_paths += 1
       self.walk(cave, set(visited), depth)

  def part2(self):
    print('===== Start part 2')

    start = self.caves['start']
    self.paths = set()
    for c in self.caves.values():
      if c.small and c.name != 'start':
        visited = set()
        self.walk2(start, visited, c, False, 0, path=[start])
    return len(self.paths)

  def walk2(self, cave, visited, allow, second_chance, depth, path):
    if cave.name == 'end':
      # print(','.join([c.name for c in path]))
      self.paths.add(','.join([c.name for c in path]))
      return
    if cave.small:
      if cave in visited:
        if cave != allow:
          return
        assert cave == allow
        if second_chance:
          return
        second_chance = True 
    visited.add(cave)
    # print('  ' * depth, cave.name)
    depth += 1

    for next_cave in cave.edges:
       self.walk2(next_cave, set(visited), allow, second_chance, depth, path + [next_cave])


day12.sample_test("""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""", expect1=10, expect2=36)

day12.sample_test("""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""", expect1=19, expect2=103)


if __name__ == '__main__':
  day12.run_and_check('input.txt', expect1=4495, expect2=131254)
