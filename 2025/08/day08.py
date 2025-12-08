#!/usr/bin/env python3
"AOC 2025: day 08"

from collections import defaultdict
from collections import namedtuple
import heapq
import itertools

from tools import aoc


Box = namedtuple('Box', 'x, y, z')


class day08(aoc.aoc):

  def __init__(self):
    super(day08, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.boxes = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    coords = [int(x) for x in line.split(',')]
    box = Box(coords[0], coords[1], coords[2])
    self.boxes.append(box)

  def post_load(self):
    # called after all input is read
    self.dists = {}
    self.distheap = []
    for i, box in enumerate(self.boxes):
      for other_i in range(i+1, len(self.boxes)):
        other_box = self.boxes[other_i]
        dist = (box.x - other_box.x) ** 2 + (box.y - other_box.y) ** 2 + (box.z - other_box.z) ** 2
        self.dists[(box, other_box)] = dist
        self.dists[(other_box, box)] = dist
        heapq.heappush(self.distheap, (dist, box, other_box))


  def part1(self):
    print('===== Start part 1')
    self.reset()
    if self.doing_sample:
      print(self.boxes)
      print(self.dists)

    box2circ = {}
    all_circuts = []
    for i in range(10):
      dx = heapq.heappop(self.distheap)
      print(f"Popped smallest item: {dx}")
      dist = dx[0],
      box1 = dx[1]
      box2 = dx[2]
      c1 = box2circ.get(box1)
      c2 = box2circ.get(box2)
      if not c1 and not c2:
        print("    New pair")
        new_circ = set([box1, box2])
        all_circuts.append(new_circ)
        box2circ[box1] = new_circ
        box2circ[box2] = new_circ
        continue
      if c1 == c2:
        print("    Nothing")
        continue 
      if c1 and not c2:
        print(f"    Merge {box2} into {c1}")
        c1.add(box2)
        box2circ[box2] = c1
        continue
      if c2 and not c1:
        print(f"    Merge {box1} into {c2}")
        c2.add(box1)
        box2circ[box1] = c2
        continue
      if self.doing_sample:
        print(f"JOIN!! {box1} {box2} {c1}, {c2}")
      c1 = c1 | c2
      for box in c2:
        box2circ[box] = c1
      c2.clear()

    # print(box2circ)
    sizes = sorted([len(circ) for circ in all_circuts], reverse=True)
    print(sizes)
    return 42


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


day08.sample_test("""
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""", expect1=40, expect2=None)


if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=None, expect2=None)
