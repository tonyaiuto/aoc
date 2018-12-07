from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys


"""
The Elves managed to locate the chimney-squeeze prototype fabric for
Santa's suit (thanks to someone who helpfully wrote its box IDs on
the wall of the warehouse in the middle of the night). Unfortunately,
anomalies are still affecting them - nobody can even agree on how to
cut the fabric.

The whole piece of fabric they're working on is a very large square -
at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for
Santa's suit. All claims have an ID and consist of a single rectangle
with edges parallel to the edges of the fabric. Each claim's rectangle
is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle
3 inches from the left edge, 2 inches from the top edge, 5 inches wide,
and 4 inches tall. Visually, it claims the square inches of fabric
represented by # (and ignores the square inches of fabric represented
by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
"""

Claim = collections.namedtuple('Claim', 'number, x, y, width, height')

def LoadClaims(inp):
  claims = []
  for line in inp:
    claim = ParseClaim(line.strip())
    claims.append(claim)
  return claims


def ParseClaim(s):
  #1 @ 916,616: 21x29

  def eat(ch):
    if not s[pos] == ch:
      raise ValueError('expecting <%s> at "%s" in "%s"' % (ch, s[pos:], s))
    pos += 1

  pos = 0
  if not s[pos] == '#':
    raise ValueError('expecting # at "%s" in "%s"' % (s[pos:], s))
  pos += 1
  number, n_chars = CollectInt(s, pos)
  pos += n_chars
  while s[pos] == ' ':
    pos += 1
  if not s[pos] == '@':
    raise ValueError('expecting @ at "%s" in "%s"' % (s[pos:], s))
  pos += 1
  x, n_chars = CollectInt(s, pos)
  pos += n_chars
  if not s[pos] == ',':
    raise ValueError('expecting , at "%s" in "%s"' % (s[pos:], s))
  pos += 1
  y, n_chars = CollectInt(s, pos)
  pos += n_chars
  if not s[pos] == ':':
    raise ValueError('expecting : at "%s" in "%s"' % (s[pos:], s))
  pos += 1
  width, n_chars = CollectInt(s, pos)
  pos += n_chars
  if not s[pos] == 'x':
    raise ValueError('expecting x at "%s" in "%s"' % (s[pos:], s))
  pos += 1
  height, n_chars = CollectInt(s, pos)
  pos += n_chars
  return Claim(number, x=x, y=y, width=width, height=height)


def CollectInt(s, pos):
  n_chars = 0
  ret = 0
  while s[pos+n_chars] == ' ':
    n_chars += 1
  while pos+n_chars < len(s) and (
      '0' <= s[pos+n_chars] and s[pos+n_chars] <= '9'):
    ret = ret * 10 + ord(s[pos+n_chars]) - ord('0')
    n_chars += 1
  # print('v=%d, pos=%d for %d' % (ret, pos, n_chars))
  return ret, n_chars


"""
If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
"""
def part1(claims):
  max_x = max_y = 0
  for c in claims:
    if max_x < c.x + c.width:
      max_x = c.x + c.width
    if max_y < c.y + c.height:
      max_y = c.y + c.height
  print('grid is %dx%d' % (max_x, max_y))
  grid = [0] * max_x * max_y

  t_a = 0
  for c in claims:
    area = 0
    # print('CLAIM: %s' % str(c))
    for y in range(c.y, c.y + c.height):
      for x in range(c.x, c.x + c.width):
        # print('  cell %d,%d' % (x,y))

        #if grid[y * max_x + x] > 0:
        #  print('overlap at %d,%d' % (x,y))
        grid[y * max_x + x] += 1
        area += 1
    # print('%s => %d' % (c, area))
    t_a += area

  print('total_area = %d' % t_a)
  double_count = 0
  for cell in grid:
    if cell > 1:
      double_count += 1
  print('double_count=%d' % double_count)


"""
Amidst the chaos, you notice that exactly one claim doesn't overlap
by even a single square inch of fabric with any other claim. If you
can somehow draw attention to it, maybe the Elves will be able to make
Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims
are made.
"""
def part2(claims):
  max_x = max_y = 0
  for c in claims:
    if max_x < c.x + c.width:
      max_x = c.x + c.width
    if max_y < c.y + c.height:
      max_y = c.y + c.height
  print('grid is %dx%d' % (max_x, max_y))
  grid = [0] * max_x * max_y

  clean = set()
  for c in claims:
    overlap = False
    for y in range(c.y, c.y + c.height):
      for x in range(c.x, c.x + c.width):
        # print('  cell %d,%d' % (x,y))
        cell_index = y * max_x + x
        old_claim = grid[cell_index]
        if old_claim != 0:
          overlap = True
          # print("unclean %d" % old_claim)
          if old_claim in clean:
            clean.remove(old_claim)
        grid[cell_index] = c.number
    if not overlap:
      clean.add(c.number)

  print(clean)


if __name__ == '__main__':
  with open(sys.argv[1]) as inp:
    claims = LoadClaims(inp)
  part1(claims)
  part2(claims)
