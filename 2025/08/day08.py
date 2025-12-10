#!/usr/bin/env python3
"AOC 2025: day 08"

from collections import namedtuple
import heapq

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

  def do_line(self, line):
    # called for each line of input
    coords = [int(x) for x in line.split(',')]
    box = Box(coords[0], coords[1], coords[2])
    self.boxes.append(box)

  def post_load(self):
    # called after all input is read
    # self.dists = {}
    self.distheap = []
    for i, box in enumerate(self.boxes):
      for other_i in range(i+1, len(self.boxes)):
        other_box = self.boxes[other_i]
        dist = (box.x - other_box.x) ** 2 + (box.y - other_box.y) ** 2 + (box.z - other_box.z) ** 2
        # self.dists[(box, other_box)] = dist
        # self.dists[(other_box, box)] = dist
        heapq.heappush(self.distheap, (dist, box, other_box))

  def part1(self):
    print('===== Start part 1')
    if self.doing_sample:
      print(self.boxes)
      # print(self.dists)

    self.box2circ = {}
    self.all_circuits = []
    limit = 1000
    if self.doing_sample:
      limit = 10
    for i in range(limit):
      self.do_next()
    sizes = sorted([len(circ) for circ in self.all_circuits], reverse=True)
    print(sizes)
    return sizes[0] * sizes[1] * sizes[2]

  def do_next(self):
      self.all_circuits = [x for x in self.all_circuits if len(x) > 0]
      dx = heapq.heappop(self.distheap)
      if self.doing_sample:
        print(f"    {[len(c) for c in self.all_circuits]}")
        print(f"Shortest pair: {dx}")
      dist = dx[0],
      box1 = dx[1]
      box2 = dx[2]
      c1 = self.box2circ.get(box1)
      c2 = self.box2circ.get(box2)
      if not c1 and not c2:
        if self.doing_sample:
          print("    New pair")
        new_circ = set([box1, box2])
        self.all_circuits.append(new_circ)
        self.box2circ[box1] = new_circ
        self.box2circ[box2] = new_circ
        return
      if c1 == c2:
        if self.doing_sample:
          print("    Nothing")
        return 

      if c1 and not c2:
        if self.doing_sample:
          print(f"    Merge {box2} into {c1}")
        c1.add(box2)
        self.box2circ[box2] = c1
        self.last_pair = [box1, box2]
        return
      elif c2 and not c1:
        if self.doing_sample:
          print(f"    Merge {box1} into {c2}")
        c2.add(box1)
        self.box2circ[box1] = c2
        self.last_pair = [box1, box2]
        return

      if self.doing_sample:
        print(f"JOIN!! {box1} {box2} {c1}, {c2}")
      if len(c1) + len(c2) == len(self.boxes):
        print(f"==> Last pair, {box1} {box2}")
        self.last_pair = [box1, box2]
      c1.update(c2)
      c1.add(box2)
      self.box2circ[box2] = c1
      for box in c2:
        self.box2circ[box] = c1
      c2.clear()
      if self.doing_sample:
        print(f"    {[len(c) for c in self.all_circuits]}")


  def part2(self):
    print('===== Start part 2')
    self.box2circ = {}
    self.all_circuits = []
    limit = len(self.boxes) ** 2
    for i in range(limit):
      self.do_next()
      sizes = sorted([len(circ) for circ in self.all_circuits], reverse=True)
      if sizes[0] == len(self.boxes):
         print(f"Done at {i}, {self.last_pair}")
         break
    print(f"=> {[len(c) for c in self.all_circuits]}")
    return self.last_pair[0].x * self.last_pair[1].x


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
		  """, expect1=40, expect2=25272)


if __name__ == '__main__':
  day08.run_and_check('input.txt', expect1=112230, expect2=2573952864)
