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
  for lmatch in range(half+1, 0, -1):
    # a match has to be at least 1 long and can be up to the full half
    center_left = lmatch - 1         # is 0 on first iteration
    center_right = l - 1 - lmatch    # is l-2 (last element) on first iteration
    lslice = lmatch * 2

    if is_reflect(values[0:lslice]):
      best_center = center_left + 1
    if is_reflect(values[-lslice:]):
      best_center = center_right + 1
  return best_center


def len_reflect(values, pos):
  lv = len(values)
  stop = min(pos, lv - pos)
  for ret in range(stop-1):
    # print('lv, stop, pos-ret, post+ret', lv, stop, pos-ret, pos+ret+1)
    if values[pos-ret] != values[pos+ret+1]:
      return ret-1
  return stop

def find_reflection_x(values):
  lv = len(values)
  best_center = -1
  best_len = -1
  for pos in range(0, lv-1):
    if values[pos] == values[pos+1]:    
      max_len = min(pos, lv-pos)
      print("Try at", pos, 'for max', max_len, 'out of', lv)
      for reflect_len in range(1, max_len):
        print("cmp", pos-reflect_len, 'to', pos+1+reflect_len)
        if values[pos-reflect_len] != values[pos+1+reflect_len]:    
          if reflect_len > best_len:
            best_len = reflect_len
  return best_center


def best_variation(rows, cols, skip_h, skip_v):
  #  bhr, bvr = best_variation(rows, cols, 
  most = max(max(rows), max(cols)) * 2

  col_dup = list(cols)
  row_dup = list(rows)
  h_reflect = -1
  v_reflect = -1
  n_reflect = 0

  bit = 1
  print("== look for new reflects that are not", skip_h, skip_v)
  for ci, col_v in enumerate(cols):
    assert bit == (1 << ci)
    for ri, row_v in enumerate(rows):
      if row_dup[ri] & bit:
        row_dup[ri] = row_v & ~bit
      else:
        row_dup[ri] = row_v | bit
      hr = find_reflection(row_dup)
      row_dup[ri] = row_v
      # did not move the reflection point
      if hr > 0 and hr == skip_h:
        continue

      if col_dup[ci] & bit:
        col_dup[ci] = col_v & ~bit
      else:
        col_dup[ci] = col_v | bit
      vr = find_reflection(col_dup)
      col_dup[ci] = col_v
      if vr > 0 and vr == skip_v:
        continue

      if hr < 0 and vr < 0:
        continue

      assert (hr > 0 and hr != skip_h) or (vr > 0 and vr != skip_v)
      assert hr < 0 or vr < 0

      if hr > 0:
        print("change", ri, ci, 'gives new h reflect at', hr, 'skiping', skip_h)
        h_reflect = hr
      if vr >= 0 and vr != skip_v:
        print("change", ri, ci, 'gives new v reflect at', vr, 'skiping', skip_v)
        v_reflect = vr

    bit <<= 1

  return h_reflect, v_reflect


def variation_points(vals, skip):
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
      if r >= 0 and r != skip:
        print('got new reflect at', r, 'skiping', skip)
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
    # Turn map in binary value of # bits per row and colum1
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
    print('rows', rows) 
    print('cols', cols) 
    vr = find_reflection(cols)
    if vr > 0:
      self.sum_vr += vr
    hr = find_reflection(rows)
    # assert vr >= 0 or hr >= 0
    if hr > 0:
      self.sum_hr += hr
    print('part1 reflection', vr, hr, '=', 100 * hr + vr)

    bhr, bvr = best_variation(rows, cols, skip_h=hr, skip_v=vr)
    if bhr > 0:
      assert bvr < 0
      self.sum_hr2 += bhr
    if bvr > 0:
      assert bhr < 0
      self.sum_vr2 += bvr
    print('= part2 reflections', bhr, bvr, 'was', hr, vr)
    if hr < 0:
      assert bhr > 0 or vr != bvr
    if vr < 0:
      assert bvr > 0 or hr != bhr

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
