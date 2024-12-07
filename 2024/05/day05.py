#!/usr/bin/env python3
"AOC 2023: day 05"

from collections import defaultdict
import graphlib

from tools import aoc


class day05(aoc.aoc):

  def __init__(self):
    super(day05, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.must_follow = defaultdict(set)
    self.must_preceed = defaultdict(set)
    self.updates = []
    self.orders_done = False

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    if not self.orders_done:
      if not line and len(self.must_follow) > 0:
        self.orders_done = True
        return
      x = line.split('|')
      first = int(x[0])
      second = int(x[1])
      self.must_follow[first].add(second)
      self.must_preceed[second].add(first)
      return

    self.updates.append([int(x) for x in line.split(',')])

  def post_load(self):
    # called after all input is read
    if self.trace > 3:
      print(self.must_follow)
      print(self.updates)
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()
    ret = 0
    self.bad = []
    for update in self.updates:
      is_ok = True
      for iv, v in enumerate(update):
        for p in self.must_follow.get(v, []):
          if p in update[0:iv]:
            # print("not ok", update)
            is_ok = False
            break
      if is_ok:
        # print('OK', update, update[(len(update)) // 2])
        ret += update[(len(update)) // 2]
      else:
        self.bad.append(update)
    return ret


  def part2(self):
    print('===== Start part 2')
    self.part1()
    print("%d bad rows" % len(self.bad))
    ret = 0
    for update in self.bad:
      ts = graphlib.TopologicalSorter()
      for v in update:
        for p in self.must_preceed.get(v, []):
          ts.add(v, p)
      ordered = list(ts.static_order())
      # print('order', update, '->', ordered)
      use = set(update)
      res = [x for x in ordered if x in use]
      ret += res[(len(res)) // 2]
    return ret


day05.sample_test("""
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""", expect1=143, expect2=123)


if __name__ == '__main__':
   # 7369 too high
  day05.run_and_check('input.txt', expect1=6505, expect2=6897)
