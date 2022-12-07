#!/usr/bin/env python3
"AOC 2021: day 07"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Dir(object):

  def __init__(self, name, parent):
    self.name = name
    self.parent = parent
    self.files = []
    self.children = {}
    self.size = 0
    self.total_size = 0

  def __str__(self):
    return 'children: %s, files: %s' % (str(self.children.keys()), str(self.files))

  def add_file(self, size, f):
    self.files.append(f)
    self.size += size

  def add_dir(self, dir):
    d = self.children.get(dir)
    if d:
      return
    d = Dir(dir, self)
    self.children[dir] = d
 


class day07(aoc.aoc):

  def __init__(self):
    super(day07, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    ALL_DIR = {}
    self.root = Dir('/', None)
    self.dir = self.root
    self.reading_dir = False

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    # print("====", line)
    if line.startswith('$ cd '):
      self.reading_dir = False
      self.cd(line[5:])
    elif line.startswith('$ ls'):
      self.reading_dir = True
    elif line.startswith('dir '):
      self.dir.add_dir(line[4:])
    else: 
      assert self.reading_dir == True
      f = line.split(' ')
      self.dir.add_file(int(f[0]), f[1])

  def post_load(self):
    # called after all input is read
    compute_sizes(self.root)
    pass

  def cd(self, dir):
    if dir == '/':
      self.dir = self.root
      return
    if dir == '..':
      self.dir = self.dir.parent
      assert self.dir != None
      return
    self.dir = self.dir.children[dir]
    

  def part1(self):
    print('===== Start part 1')
    return sum_small(self.root)

  def part2(self):
    print('===== Start part 2')
    need = 30000000
    cap = 70000000
    used = self.root.total_size
    free = cap - used
    want = need - free
    # print('cap/used/free/want', cap, used, free, want)
    return find_min_over(self.root, want, min=cap)


def compute_sizes(fs, depth=0):
  # print(' ' * depth, fs)
  fs.total_size = fs.size 
  for child in fs.children.values():
    fs.total_size += compute_sizes(child, depth=depth+1)
  # print('TOT:', fs.name, fs.total_size)
  return fs.total_size

def sum_small(fs, sum=0):
  if fs.total_size <= 100000:
    sum += fs.total_size
  for child in fs.children.values():
    sum = sum_small(child, sum=sum)
  return sum

def find_min_over(fs, want, min):
  if fs.total_size >= want:
    # print('  => %10d %s' % (fs.total_size, fs.name))
    if fs.total_size < min:
      min = fs.total_size
  for child in fs.children.values():
    min = find_min_over(child, want, min)
  return min


day07.sample_test("""
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""", expect1=95437, expect2=24933642)


if __name__ == '__main__':
  day07.run_and_check('input.txt', expect1=1453349, expect2=2948823)
  pass
