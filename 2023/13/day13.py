#!/usr/bin/env python3
"AOC 2023: day 13"

from tools import aoc

def is_reflect(slice):
  l = len(slice)
  half = l // 2
  if half * 2 != l:
    return False
  for i in range(half):
    if slice[half-1-i] != slice[half+i]:
      return False
  return True


def find_reflection(values):
  # A reflection needs to hit at least one edge
  l = len(values)
  half = (l + 1) // 2
  best_center = -1
  for lmatch in range(1, half+1):
    # a match has to be at least 1 long and can be up to the full half
    center_left = lmatch - 1         # is 0 on first iteration
    center_right = l - 1 - lmatch    # is l-2 (last element) on first iteration
    lslice = lmatch * 2

    if is_reflect(values[0:lslice]):
      best_center = center_left + 1
    if is_reflect(values[-lslice:]):
      best_center = center_right + 1
  return best_center


def best_variation(vals, skip):
  # [109, 12, 30, 30, 76, 97, 30, 30, 115]
  l = len(vals)
  bit = 1
  v2 = list(vals)
  most = max(vals) * 2
  reflect = -1
  n_reflect = 0
  print(vals, 'start best variation')
  while bit < most:
    for vi, v in enumerate(vals):
      if vals[vi] & bit:
        v2[vi] = v & ~bit
      else:
        v2[vi] = v | bit
      # print(v2, 'bit', bit)
      r = find_reflection(v2)
      v2[vi] = v
      if r > 0 and r != skip:
        # print('got new reflect at', r)
        if reflect != r:
          reflect = r
          n_reflect += 1
          assert n_reflect < 2
    bit <<= 1
  return reflect


class day13(aoc.aoc):

  def __init__(self):
    super(day13, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.sum_vr = 0
    self.sum_hr = 0
    self.sum_vr2 = 0
    self.sum_hr2 = 0

  def do_line(self, map):
    # called for each line of input
    print("===============")
    nc = len(map[0])
    cols = [0] * nc
    rows = []
    for row in map:
      rv = 0
      for col, c in enumerate(row):
        cols[col] *= 2
        rv *= 2
        if c == '#':
           cols[col] += 1
           rv += 1
      rows.append(rv)
      print('%5d' % rv, row)
    print(cols) 
    vr = find_reflection(cols)
    if vr > 0:
      self.sum_vr += vr
    hr = find_reflection(rows)
    # assert vr >= 0 or hr >= 0
    if hr > 0:
      self.sum_hr += hr
    print(vr, hr)

    bvr = best_variation(cols, skip=vr)
    if bvr > 0:
      self.sum_vr2 += bvr
    bhr = best_variation(rows, skip=hr)
    if bhr > 0:
      self.sum_hr2 += bhr

    if (bvr > 0 and vr < 0) and (bhr > 0 and hr < 0):
      print("==============  Lost VR and HR")
      assert False
    if (bvr < 0 and vr < 0) and (bhr < 0 and hr < 0):
      print("==============  FAILED")
      assert False
    print(vr, hr)

  def part1(self):
    print('===== Start part 1')
    ret = self.sum_vr + 100 * self.sum_hr
    print('part1', ret)
    return ret

  def part2(self):
    print('===== Start part 2')
    ret = self.sum_vr2 + 100 * self.sum_hr2
    # if ret <= 33703:
    if ret <= 35515:
      print("TOO LOW")
    print('part2', ret)
    return ret


day13.sample_test("""
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""", expect1=405, expect2=400)


if __name__ == '__main__':
  day13.run_and_check('input.txt', expect1=34821, expect2=None)
