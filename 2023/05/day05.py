#!/usr/bin/env python3
"AOC 2023: day 05"

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
    self.maps = {}
    self.cur_map = None

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    l = line.strip()
    if not l:
      return

    if l.startswith('seeds:'):
      self.seeds = [int(x) for x in l.split(' ')[1:]]
      print('seeds', self.seeds)
      return

    if line.endswith('map:'):
      name = line.split(' ')[0].replace('-', '_')
      self.maps[name] = []
      self.cur_map = self.maps[name]
      return

    row = [int(x) for x in line.split(' ')]
    self.cur_map.append(row)
    assert len(row) == 3
    assert row[2] > 0

  def post_load(self):
    # called after all input is read

    """
    m = self.merge_maps(
      self.maps['seed_to_soil'],
      self.maps['soil_to_fertilizer'])
    m = self.merge_maps(m, self.maps['fertilizer_to_water'])
    m = self.merge_maps(m, self.maps['water_to_light'])
    m = self.merge_maps(m, self.maps['light_to_temperature'])
    m = self.merge_maps(m, self.maps['temperature_to_humidity'])
    m = self.merge_maps(m, self.maps['humidity_to_location'])
    self.merged = m
    for row in m:
      print(row)
    """

  @staticmethod
  def merge_maps(map_a, map_b):

    ret = []
    for a in map_a:
      a_dest = a[0]
      a_source = a[1]
      a_len = a[2]
      a_end = a_dest + a_len
      did_split = False
      for b in map_b:
        b_source = b[1]
        b_len = b[2]
        if a_end <= b_source:
          continue
        if a_dest >= b_source + b_len:
          continue
        #
        #
        #       aaaaaa
        #    bbbb
        split_delta = a_dest - b_source    # 35 = 50 - 15
        print('split', a, b, '@', split_delta)

        if split_delta >= 0:
          #  dest:   aaaa
          #  src:  112222333
          # split [50, 98, 2] [0, 15, 37]

          # want 1: [0, 15, 35=split_delta]
          if split_delta > 0:
            ret.append([b[0], b_source, split_delta])

          # want 2: [0 + (50-15), 98, 2]
          b_left_len = b_len - split_delta

          if b_left_len < a_len:
            ll = a_len - b_left_len
            if b_left_len > 0:
              ret.append([b[0] + a_dest - b_source, a_source, b_left_len])
            ret.append([a_dest+b_left_len, a_source+b_left_len, ll])
          if b_left_len == a_len:
            ret.append([b[0] + a_dest - b_source, a_source, a_len])
          if b_left_len > a_len:
            ll = b_left_len - a_len
            ret.append([a_dest+b_left_len, a_source+b_left_len, a_len])
            ret.append([b[0] + a_dest - b_source, a_source, ll])
            print(" === ", a, b, ret[-3:])
          print('  =>', ret)

        if split_delta < 0:
          # split [0, 15, 35] [0, 11, 42] @ -11
          # aaaaa
          # bbbbbbbb
          #    [0, 15, 11] [
          b_left_len = b_len - split_delta


          # ret.append([b_source, b_dest, a_source-btest])

          if b_left_len < a_len:
            ll = a_len - b_left_len
            if b_left_len > 0:
              ret.append([b[0] + a_dest - b_source, a_source, b_left_len])
            ret.append([a_dest+b_left_len, a_source+b_left_len, ll])
          if b_left_len == a_len:
            ret.append([b[0] + a_dest - b_source, a_source, a_len])
          if b_left_len > a_len:
            ll = b_left_len - a_len
            ret.append([a_dest+b_left_len, a_source+b_left_len, a_len])
            ret.append([b[0] + a_dest - b_source, a_source, ll])
            print(" === ", a, b, ret[-3:])
          print('  =>', ret)


        did_split = True

      if not did_split:
        ret.append(a)
    print(ret)
    return ret


  def part1(self):
    print('===== Start part 1')

    mloc = -1
    for s in self.seeds:
      x = self.seed_to_location(s)
      print("seed", s, '=>', x)
      if x < mloc or mloc < 0:
        mloc = x
    print('part1', mloc)
    return mloc

  def part2x(self):
    print('===== Start part 2')
    mloc = -1
    ls = len(self.seeds)
    for i in range(ls//2):
      si = i * 2
      start = self.seeds[si]
      l_range  = self.seeds[si+1]
      print("=== Seed range", start, 'to', start+l_range, 'len', l_range)
      for ic in range(l_range):
        s = start+ic
        if ic % 1000000 == 0:
          print("     ic", ic)
        # if merged maps worked, use this
        # x = self.find_in_range_list(self.merged, s)


  def part2(self):
    print('===== Start part 2')
    mloc = -1
    ls = len(self.seeds)
    for i in range(ls//2):
      si = i * 2
      start = self.seeds[si]
      l_range  = self.seeds[si+1]
      print("Seed range", start, 'to', start+l_range, 'len', l_range)
      for ic in range(l_range):
        s = start+ic
        if ic % 1000000 == 0:
          print("     ic", ic)
        # if merged maps worked, use this
        # x = self.find_in_range_list(self.merged, s)
        x = self.seed_to_location(s)
        # print("seed", s, '=>', x)
        if x < mloc or mloc < 0:
          mloc = x
      print("Seed range", start, 'to', start+l_range, 'MIN', mloc)

    print('part2', mloc)
    return mloc

  
  def find_in_map(self, map_name, v):
    ranges = self.maps[map_name]
    ret = self.find_in_range_list(ranges, v)
    # print(map_name, ret, ret)
    return ret

  @staticmethod
  def find_in_range_list(range_list, v):
    for row in range_list:
      if row[1] <= v and v < row[1] + row[2]:
        delta = v - row[1]
        # print(map_name, v, row[0] + delta)
        return row[0] + delta
    return v

  def seed_to_location(self, seed):
    soil = self.find_in_map('seed_to_soil', seed)
    fert = self.find_in_map('soil_to_fertilizer', soil)
    water = self.find_in_map('fertilizer_to_water', fert)
    light = self.find_in_map('water_to_light', water)
    temp = self.find_in_map('light_to_temperature', light)
    humid = self.find_in_map('temperature_to_humidity', temp)
    loc = self.find_in_map('humidity_to_location', humid)
    return loc



day05.sample_test("""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""", expect1=35, expect2=46)


if __name__ == '__main__':
  day05.run_and_check('input.txt', expect1=318728750, expect2=None)
