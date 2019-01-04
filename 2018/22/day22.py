"""aoc 2018 day 22"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

from memoized import memoized

_VERBOSE = 0
_PART2 = False


class Cave(object):

  ROCKY = 0
  WET = 1
  NARROW = 2

  TORCH = 0
  CLIMB = 1
  NEITHER = 2

  tool_names = ['TORCH', 'CLIMB', 'NEITHER']

  # memoize cost function
  costs = {(0, 0): (0, TORCH)}

  def __init__(this, depth=1, target_x=0, target_y=0):
    this.depth = depth
    this.target_x = target_x
    this.target_y = target_y
    this.mouth = (0,0)

  def __str__(this):
    return 'Cave(depth=%d, target=%d,%d)' % (this.depth, this.target_x,
                                             this.target_y)

  @staticmethod
  def Load(inp):
    ret = Cave()
    for l in inp:
      if l.startswith('depth:'):
        ret.depth = int(l[6:].strip())
      elif l.startswith('target:'):
        xy = [int(v) for v in l[7:].strip().split(',')]
        ret.target_x = xy[0]
        ret.target_y = xy[1]
    return ret

  def Print(this):
    pass

  def geologic_index(this, x, y):
    # The man explains that due to the unusual geology in the area, there
    # is a method to determine any region's type based on its erosion
    # level. The erosion level of a region can be determined from its
    # geologic index. The geologic index can be determined using the first
    # rule that applies from the list below:

    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    # If the region's Y coordinate is 0, the geologic index is its X coordinate
    # times 16807.
    if y == 0:
      return x * 16807
    # If the region's X coordinate is 0, the geologic index is its Y coordinate
    # times 48271.
    if x == 0:
      return y * 48271
    # Otherwise, the region's geologic index is the result of multiplying the
    # erosion levels of the regions at X-1,Y and X,Y-1.
    if x == this.target_x and y == this.target_y:
      return 0
    return this.erosion(x-1, y) * this.erosion(x, y-1)

  @memoized
  def erosion(this, x, y):
    # A region's erosion level is its geologic index plus the cave system's
    # depth, all modulo 20183. Then:
    return (this.geologic_index(x, y) + this.depth) % 20183

  def type(this, x, y):
    # If the erosion level modulo 3 is 0, the region's type is rocky.
    # If the erosion level modulo 3 is 1, the region's type is wet.
    # If the erosion level modulo 3 is 2, the region's type is narrow.
    return this.erosion(x, y) % 3

  def TotalRisk(this):
    ret = 0
    for y in range(this.target_y + 1):
      for x in range(this.target_x + 1):
        ret += this.type(x, y)
    return ret

  def MinimalCostToReach(this, x, y):
    # Returns: minimal cost to reach x, y from 0,0 and what tool you would
    # have.
    if x == 0 and y == 0:
      return 0, Cave.TORCH

    cached = Cave.costs.get((x,y))
    if cached:
      return cached[0], cached[1]

    dest_type = cave.type(x, y)
    new_costs = []
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
      if x < 0 or y < 0:
        continue
      cached = Cave.costs.get((x+dx, y+dy))
      if not cached:
        continue
      # cost, tool = this.MinimalCostToReach(x+dx, y+dy)
      cost = cached[0]
      tool = cached[1]

      if cost < 0:
        continue
      from_type = cave.type(x+dx, y+dy)
      if from_type == dest_type:
        new_costs.append((cost+1, tool))
      elif dest_type == Cave.ROCKY:
        if tool == Cave.TORCH or tool == Cave.CLIMB:
          new_costs.append((cost+1, tool))
        else:
          # tool==NEITHER => from_type==WET|NARROW
          if from_type == Cave.WET:
            new_costs.append((cost+8, Cave.CLIMB))
          else:
            new_costs.append((cost+8, Cave.TORCH))
      elif dest_type == Cave.WET:
        if tool == Cave.NEITHER or tool == Cave.CLIMB:
          new_costs.append((cost+1, tool))
        else:
          # tool==TORCH => from_type==ROCKY|NARROW
          new_costs.append((cost+8, Cave.NEITHER))
          if from_type == Cave.ROCKY:
            new_costs.append((cost+8, Cave.CLIMB))
      elif dest_type == Cave.NARROW:
        if tool == Cave.NEITHER or tool == Cave.TORCH:
          new_costs.append((cost+1, tool))
        else:
          # tool==CLIMB => from_type==ROCKY|WET
          new_costs.append((cost+8, Cave.NEITHER))
          if from_type == Cave.ROCKY:
            new_costs.append((cost+8, Cave.TORCH))
      else:
        raise ValueError(
            'Impossible region type: %d at %d,%d' % (dest_type, x, y))

    if not new_costs:
      return -2, None

    best_cost = new_costs[0][0]
    tools = set()
    for c in sorted(new_costs):
      # print('%d with %s' % (c[0], Cave.tool_names[c[1]]))
      if c[0] > best_cost:
        break
      tools.add(c[1])
    # print('best = %d, tools=%s' % (best_cost, tools))
    best_tool = -1
    for t in tools:
      if t > best_tool:
        best_tool = t
    Cave.costs[(x,y)] = (best_cost, best_tool)
    return best_cost, best_tool

  def PrimeCosts(this):
    for x in range(this.target_x+20):
      for y in range(this.target_y+20):
        this.MinimalCostToReach(x, y)


"""
class Path(object):

  def __init__(this):
    this.time =  0
    this.head_x = 0
    this.head_y = 0
    this.tool = Path.TORCH
    this.region_type = ROCKY

  def CostToMoveTo(this, cave, x, y):
    # Tools can only be used in certain regions:
    # - In rocky regions, you can use the climbing gear or the torch. You
    #   cannot use neither (you'll likely slip and fall).
    # - In wet regions, you can use the climbing gear or neither tool. You
    #   cannot use the torch (if it gets wet, you won't have a light source).
    # - In narrow regions, you can use the torch or neither tool. You cannot
    #   use the climbing gear (it's too bulky to fit).
    if x < 0 or y < 0:
      return -1, None
    region_type = cave.type(x, y)
    if this.region_type == region_type:
      return 1, None
    if region_type == Cave.ROCKY:
      if this.tool == Path.TORCH:
        return 1, None
      elif this.tool == Path.CLIMB:
        return 1, None
      else:
        return 8, [Path.TORCH, Path.CLIMB]
    elif region_type == Cave.WET:
      if this.tool == Path.TORCH:
        return 8, [Path.NEITHER, Path.CLIMB]
      else:
        return 1, None
    elif region_type == Cave.NARROW:
      if this.tool == Path.CLIMB:
        return 8, [Path.NEITHER, Path.TORCH]
      else:
        return 1, None
    else:
      raise ValueError(
          'Impossible region type: %d at %d,%d' % (region_type, x, y))
"""



def SelfCheck():
  # For example, suppose the cave system's depth is 510 and the target's
  # coordinates are 10,10. Using % to represent the modulo operator,
  # the cavern would look as follows:
  cave = Cave(depth=510, target_x=10, target_y=10)

  # At 0,0, the geologic index is 0. The erosion level is (0 + 510)
  # % 20183 = 510. The type is 510 % 3 = 0, rocky.
  assert cave.type(0, 0) == Cave.ROCKY

  # At 1,0, because the Y coordinate is 0, the geologic index is 1
  # * 16807 = 16807. The erosion level is (16807 + 510) % 20183 =
  # 17317. The type is 17317 % 3 = 1, wet.
  assert cave.type(1, 0) == Cave.WET

  # At 0,1, because the X coordinate is 0, the geologic index is 1
  # * 48271 = 48271. The erosion level is (48271 + 510) % 20183 =
  # 8415. The type is 8415 % 3 = 0, rocky.
  assert cave.type(0, 1) == Cave.ROCKY

  # At 1,1, neither coordinate is 0 and it is not the coordinate
  # of the target, so the geologic index is the erosion level of 0,1
  # (8415) times the erosion level of 1,0 (17317), 8415 * 17317 =
  # 145722555. The erosion level is (145722555 + 510) % 20183 = 1805.
  # The type is 1805 % 3 = 2, narrow.
  assert cave.type(1, 1) == Cave.NARROW
  assert cave.type(0, 1) == Cave.ROCKY

  # At 10,10, because they are the target's coordinates, the geologic
  # index is 0. The erosion level is (0 + 510) % 20183 = 510. The type
  # is 510 % 3 = 0, rocky.
  assert cave.geologic_index(10, 10) == 0
  assert cave.erosion(10, 10) == 510
  assert cave.type(10, 10) == Cave.ROCKY

  # In the cave system above, because the mouth is at 0,0 and the target
  # is at 10,10, adding up the risk level of all regions with an X
  # coordinate from 0 to 10 and a Y coordinate from 0 to 10, this total
  # is 114.
  assert cave.TotalRisk() == 114

  cave.PrimeCosts()
  assert cave.MinimalCostToReach(0, 0) == (0, Cave.TORCH)
  assert cave.MinimalCostToReach(1, 0) == (8, Cave.NEITHER)
  assert cave.MinimalCostToReach(0, 1) == (1, Cave.TORCH)
  assert cave.MinimalCostToReach(1, 1) == (2, Cave.TORCH)
  print(cave.MinimalCostToReach(4, 1))
  # assert cave.MinimalCostToReach(4, 1) == (12, Cave.NEITHER)


if __name__ == '__main__':
  iarg = 1
  dump = False
  while iarg < len(sys.argv) and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-d':
      dump = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1

  with open(sys.argv[iarg]) as inp:
    cave = Cave.Load(inp)
  if dump:
    print(cave)
  SelfCheck()

  # part1
  print('risk: %d' % cave.TotalRisk())


"""
You start at 0,0 (the mouth of the cave) with the torch equipped
and must reach the target coordinates as quickly as possible. The
regions with negative X or Y are solid rock and cannot be traversed.
The fastest route might involve entering regions beyond the X or Y
coordinate of the target.

You can move to an adjacent region (up, down, left, or right; never
diagonally) if your currently equipped tool allows you to enter
that region. Moving to an adjacent region takes one minute. (For
example, if you have the torch equipped, you can move between rocky
and narrow regions, but cannot enter wet regions.)

You can change your currently equipped tool or put both away if
your new equipment would be valid for your current region. Switching
to using the climbing gear, torch, or neither always takes seven
minutes, regardless of which tools you start with. (For example,
if you are in a rocky region, you can switch from the torch to the
climbing gear, but you cannot switch to neither.)

Finally, once you reach the target, you need the torch equipped
before you can find him in the dark. The target is always in a rocky
region, so if you arrive there with climbing gear equipped, you
will need to spend seven minutes switching to your torch.

For example, using the same cave system as above, starting in the
top left corner (0,0) and moving to the bottom right corner (the
target, 10,10) as quickly as possible, one possible route is as
follows, with your current position marked X:

Initially:
X=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down:
M=.|=.|.|=.|=|=.
X|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.X=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using the torch to neither tool:
M=.|=.|.|=.|=|=.
.X=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right 3:
M=.|=.|.|=.|=|=.
.|=|X|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using neither tool to the climbing gear:
M=.|=.|.|=.|=|=.
.|=|X|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down 7:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..X==..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..=X=..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down 3:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||.X.|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||..X|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Down:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.X..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Right 4:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=X||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Up 2:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===X===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Switch from using the climbing gear to the torch:
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===X===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

This is tied with other routes as the fastest way to reach the
target: 45 minutes. In it, 21 minutes are spent switching tools
(three times, seven minutes each) and the remaining 24 minutes are
spent moving.

What is the fewest number of minutes you can take to reach the target?

"""
