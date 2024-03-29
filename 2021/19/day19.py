#!/usr/bin/env python3
"AOC 2021: day 19"

import itertools

from tools import aoc

import rotate


def pdiff(a, b):
  return (b[0]-a[0], b[1]-a[1], b[2]-a[2])


def m_dist(a, b):
  return abs(b[0]-a[0]) + abs(b[1]-a[1]) + abs(b[2]-a[2])


class Scanner(object):

  def __init__(self, inp):
    assert inp[0].startswith('--- scanner ')
    t = inp[0][12:].split(' ')
    self.n = int(t[0])
    self.positions = []
    self.rotation = -1
    self.merged = False
    self.pos = (0, 0, 0)
    for line in inp[1:]:
      if not line:
        continue
      x = tuple([int(n) for n in line.split(',')])
      self.positions.append(x)
    self.beacons = BeaconList(self, 0)

  def __str__(self):
    return 'scr:%d, %s' % (self.n, self.positions)

  def check_for_matches(self, other, rotation):
    """Check for matches against another at a rotation."""
    other.beacons = BeaconList(other, rotation)
    other.rotation = rotation
    return self.beacons.find_matches(
        other.beacons, msg='(%2d %2d)' % (self.n, other.n))

  def rotate_to_me(self, other):
    """Try all rotations for the other and return the best fit."""
    best_n_match = 0
    best_translation = None
    best_matched = 0
    best_beacons = None
    for rotation in range(24):
      n_match, translation, matched = self.check_for_matches(other, rotation)
      if n_match > best_n_match:
        best_n_match = n_match
        best_translation = translation
        best_matched = matched
        best_beacons = other.beacons
      if n_match >= 12:
        print('=========== align', self.n, other.n, 'rot:', rotation, 'n_match:', n_match)
    if best_beacons:
      other.beacons = best_beacons
    return best_n_match, best_translation, best_matched

  def merge_in(self, other, translation, expected_matches):
    """Merge other into me."""

    print('merge', self.n, '<-', other.n, 'translation:', translation)
    other.pos = pdiff(translation, (0, 0, 0))
    other.merged = True
    # assert, other.beacons is rotated correctly
    other_beacons = other.beacons
    n_match = 0
    to_add = []
    for pos in other_beacons.positions:
      n_pos = pdiff(translation, pos)
      if n_pos in self.beacons.positions:
        # assert pos in expected_matches
        n_match += 1
      else:
        to_add.append(n_pos)
    self.positions.extend(to_add)
    print('eliminated', n_match, 'leaving', len(to_add), 'total beacons:', len(self.positions))
    self.beacons = BeaconList(self, self.rotation)


class BeaconList(object):
  """A rotated set of beacons and the set of deltas between each."""

  def __init__(self, scanner, rotation):
    self.scanner = scanner
    self.rotation = rotation
    rf = rotate.rot_func[rotation]
    rotated = [rf(pos) for pos in scanner.positions]
    self.positions = rotated

    # compute all the deltas
    lp = len(self.positions)
    deltas = {}
    for fp in range(0, lp):
      fpos = self.positions[fp]
      for tp in range(fp+1, lp):
        tpos = self.positions[tp]
        delta = pdiff(fpos, tpos)
        if delta in deltas:
          print("FUCK, do it the hard way")
          print(deltas)
          sys.exit(1)

        deltas[delta] = (fpos, tpos)
    self.deltas = deltas
    # assert len(self.deltas) == lp * (lp - 1) // 2

  def find_matches(self, other, msg=''):
    my_deltas = self.deltas
    other_deltas = other.deltas
    scanner_translation = None
    possible_translation_1 = None
    possible_translation_2 = None
    n_match = 0
    matched = set()
    for d in other_deltas:
      point_pair = my_deltas.get(d)
      if point_pair:
        f1, f2 = point_pair
        t1, t2 = other_deltas[d]
        if t1 not in matched:
          n_match += 1
          matched.add(t1)
        if t2 not in matched:
          n_match += 1
          matched.add(t2)
        # print('s %s:' % msg, d, f1, f2, '...', t1, t2)

        # What is the delta between the points from self and other?
        # They all must be the same
        d1 = pdiff(f1, t1)
        d2 = pdiff(f1, t2)
        d3 = pdiff(f2, t2)

        assert d1 == d3
        if not possible_translation_1:
          possible_translation_1 = d1
          possible_translation_2 = d2
        else:
          if not scanner_translation:
            if d1 == possible_translation_1:
              scanner_translation = d1
              assert d2 != possible_translation_2
            elif d1 == possible_translation_2:
              scanner_translation = d1
            else:
              assert d2 == possible_translation1 or d2 == possible_translation_2
              scanner_translation = d2
          assert d1 == scanner_translation or d2 == scanner_translation
    if matched:
      print('match:', msg, 'at rotation', other.rotation, '->', n_match, 'matches')
      assert len(matched) == n_match
    return n_match, scanner_translation, matched


class day19(aoc.aoc):

  def __init__(self):
    super(day19, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.scanners = []

  def do_line(self, line):
    # called for each line of input
    self.scanners.append(Scanner(line))

  def part1(self):
    print('===== Start part 1')

    # Better solution idea:
    # Do not find an anchor pair. Start with 0
    # Do the merge passes as below.
    # If nothing matches with scanner 0, repeat for scanner 1, ...

    # Find a pair that match at no rotation.
    anchor = None
    for scanner, other in itertools.combinations(self.scanners, 2):
      n_match, translation, matches = scanner.check_for_matches(other, 0)
      if n_match >= 12:
        print('You sunk my battleship', scanner.n, other.n, 'by', n_match)
        scanner.rotation = 0
        other.rotation = 0
        anchor = scanner
        scanner.merge_in(other, translation, matches)
        break

    # We have the first pair. So we rotate the others to match these.
    print('Checking with anchor', anchor.n)
    more_scanners = True
    min_match = 12
    while more_scanners:
      more_scanners = False
      did_merge = False
      for scanner in self.scanners:
        if scanner == anchor or scanner.merged:
          continue
        more_scanners = True
        n_match, translation, matched = anchor.rotate_to_me(scanner)
        if (n_match >= min_match) and translation:
          print("MERGING", len(matched))
          anchor.merge_in(scanner, translation, matched)
          scanner.merged = True
          did_merge = True
        else:
          print('Did not match', anchor.n, 'to', scanner.n)
      if not did_merge:
        min_match -= 1
    return len(anchor.positions)

  def part2(self):
    print('===== Start part 2')
    return max([m_dist(a.pos, b.pos)
                for a, b in itertools.combinations(self.scanners, 2)])



day19.sample_test('sample.txt', is_file=True, expect1=79, expect2=3621, recreate=False)


if __name__ == '__main__':
  day19.run_and_check('input.txt', expect1=357, expect2=12317, recreate=False)
