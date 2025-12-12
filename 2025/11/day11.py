#!/usr/bin/env python3
"AOC 2025: day 11"

from collections import defaultdict
from collections import namedtuple
import copy

from tools import aoc
from tools import gridutils

Dev = namedtuple("Dev", "name, outs")

class day11(aoc.aoc):

  def __init__(self):
    super(day11, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.all_devs = []
    self.devs = {}

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    # hhh: ccc fff iii
    parts = line.split(' ')
    dev_name = parts[0][:-1]
    dev = Dev(name=dev_name, outs=set(parts[1:]))
    self.devs[dev_name] = dev
    self.all_devs.append(dev)

  def build_reverse_map(self):
    # build the antimap of device to devices leading to it.
    feeders = defaultdict(set)
    for dev in self.devs.values():
      for out in dev.outs:
        feeders[out].add(dev.name)
    if self.doing_sample:
      print(feeders)
    return feeders

  def reduce(self):
    feeders = self.build_reverse_map()

    nd = {}
    to_delete = []
    for dev_n in list(self.devs.keys()):
      dev = self.devs[dev_n]
      # node just forwards
      if dev.name in ("fft", "dac"):
        continue
      if len(dev.outs) == 1:
        new_targ = list(dev.outs)[0]
        # repoint other devs to my destination
        for feeder in feeders[dev.name]:
          feed_dev = self.devs.get(feeder)
          if feed_dev:
            nd = Dev(name=feed_dev.name, outs=set(
              [new_targ if out==dev.name else out for out in feed_dev.outs]))
            # print(f"Repoint {feeder} to {new_targ}, {dev} => {nd}")
            self.devs[feed_dev.name] = nd
        # now clean it
        feeders[new_targ].update(feeders[dev.name])
        del feeders[dev.name]
        del self.devs[dev.name]
        # to_delete.append(dev.name)

  def reduce_all(self):
    while len(self.devs) > 30:
      orig_size = len(self.devs)
      print(f"== {orig_size} devs")
      self.reduce()
      new_size = len(self.devs)
      if orig_size == new_size:
        print(f"==>> reduced to {new_size} devs")
        break
    with open("reduced_input.txt", "w") as out:
      for dev in self.devs.values():
        out.write(f"{dev.name}: {' '.join(dev.outs)}\n")

  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      print(self.devs)
    start = self.devs.get("you")
    if not start:
      return 0
    return self.find_paths(cur=start, visited=set())

  def find_paths(self, cur, visited, end="out", need_fft=False):
    visited = set(visited)
    visited.add(cur.name)
    if len(visited) > 20:
      print(visited)
    found = 0
    for out in cur.outs:
      if out == end:
        # print(visited)
        if need_fft:
          if "fft" in visited and "dac" in visited:
            found += 1
        else:
          found += 1
        continue
      if out in visited:
        continue
      out_dev = self.devs[out]
      found += self.find_paths(cur = out_dev, visited=visited, need_fft=need_fft)
    return found

  def part2(self):
    print('===== Start part 2')
    self.reset()
    if self.doing_sample:
      for d in self.devs.values():
        print(f"  {d}")
    start = self.devs.get("svr")
    if not start:
      return 0
    self.feeders = self.build_reverse_map()

    print("Finding from fft")
    from_fft = self.find_paths(cur=self.devs.get("fft"), visited=set())
    from_dac = self.find_paths(cur=self.devs.get("dac"), visited=set())
    print(f"from_fft: {from_fft}, from_dac: {from_dac}")

    to_fft = self.find_paths(cur=self.devs.get("svr"), end="fft", visited=set())
    to_dac = self.find_paths(cur=self.devs.get("svr"), end="dac", visited=set())
    print(f"to_fft: {to_fft}, to_dac: {to_dac}")

    if self.doing_sample:
       return self.find_paths(cur=start, visited=set(), need_fft=True)
    return self.find_paths(cur=start, visited=set(), need_fft=True)



day11.sample_test("""
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""", expect1=5, expect2=None)

day11.sample_test("""
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""", expect1=None, expect2=2)

if __name__ == '__main__':
  day11.run_and_check('input.txt', expect1=714, expect2=None)
