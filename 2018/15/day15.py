"""aoc 2018 day 15"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

_VERBOSE = 0

_ATTACK_FAVOR_X = False

class Unit(object):

  id = 1

  def __init__(this, kind, x, y):
    Unit.id += 1
    this.id = Unit.id
    this.kind = kind
    this.x = x
    this.y = y
    this.power = 3
    this.hp = 200

  def __str__(this):
    # return '%c@%d,%d#%d' % (this.kind, this.x, this.y, this.id)
    return '%c@%d,%d' % (this.kind, this.x, this.y)

  def __lt__(this, other):
    return ((this.y < other.y) or (this.y == other.y and this.x < other.x))
  def __eq__(this, other):
    return this.y == other.y and this.x == other.x
  def __ne__(this, other):
    return not this == other
  def __gt__(this, other):
    return other < this
  def __ge__(this, other):
    return not this < other
  def __le__(this, other):
    return not other < this

  def CanAttack(this, game):
    can_attack = []
    other_kind = Game.ELF if this.kind == Game.GOBLIN else Game.GOBLIN
    for nx, ny in [(this.x, this.y-1), (this.x-1, this.y),
                   (this.x+1, this.y), (this.x, this.y+1)]:
      if game.Get(nx, ny) == other_kind:
        for u in game.units:
          if u.x == nx and u.y == ny:
            can_attack.append(u)
    return can_attack

  def Move(this, game):
    """Move.
    To move, the unit first considers the squares that are in range and
    determines which of those squares it could reach in the fewest
    steps. A step is a single movement to any adjacent (immediately up,
    down, left, or right) open (.) square. Units cannot move into walls
    or other units. The unit does this while considering the current
    positions of units and does not do any prediction about where units
    will be later. If the unit cannot reach (find an open path to) any
    of the squares that are in range, it ends its turn. If multiple
    squares are in range and tied for being reachable in the fewest
    steps, the step which is first in reading order is chosen.

    Targets:      In range:     Reachable:    Nearest:      Chosen:
    #######       #######       #######       #######       #######
    #E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
    #...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
    #.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
    #######       #######       #######       #######       #######
    In the above scenario, the Elf has three targets (the three Goblins):

    """
    this.moved = False
    can_attack = this.CanAttack(game)
    if can_attack:
      return can_attack

    other_kind = Game.ELF if this.kind == Game.GOBLIN else Game.GOBLIN
    distances = game.Flood(this.x, this.y, other_kind)
    closest = None
    nearest_distance = game.width + game.height
    for u in game.units:
      if this == u or this.kind == u.kind or u.hp < 0:
        continue
      d = distances.get((u.x, u.y), 999)
      if _VERBOSE > 1:
        print('  => %s distance %d to %s' % (this, d, u))
      if d < nearest_distance:
        nearest_distance = d
        closest = u
    if closest:
      this.moved = True
      this.MoveTowards(closest, game)
    return this.CanAttack(game)

  def MoveTowards(this, targ, game):
    """Pick the free square that is the closest to target.

    Then, the unit identifies all of the open squares (.) that are in
    range of each target; these are the squares which are adjacent
    (immediately up, down, left, or right) to any target and which
    aren't already occupied by a wall or another unit. Alternatively,
    the unit might already be in range of a target. If the unit is not
    already in range of a target, and there are no open squares which
    are in range of a target, the unit ends its turn.

    If the unit is already in range of a target, it does not move, but
    continues its turn with an attack. Otherwise, since it is not in
    range of a target, it moves.
    Ties done in reading order.
    """
    distances = game.Flood(targ.x, targ.y,
                           Game.ELF if this.kind == Game.GOBLIN else Game.GOBLIN)
    # print(distances)
    nearest = game.width + game.height + 1
    to_x = to_y = -1
    # reading order. up, left, right, down
    for nx, ny in [(this.x, this.y-1), (this.x-1, this.y),
                   (this.x+1, this.y), (this.x, this.y+1)]:
      d = distances.get((nx, ny))
      if d is not None and d < nearest:
        nearest = d
        to_x = nx
        to_y = ny
    if _VERBOSE > 1:
      print('  => %s towards %s via %d,%d' % (this, targ, to_x, to_y))
    if nx >= 0:
      game.MoveUnit(this, to_x, to_y)


  def Attack(this, game, to_attack):
    # To attack, the unit first determines all of the targets that are
    # in range of it by being immediately adjacent to it. If there are
    # no such targets, the unit ends its turn. Otherwise, the adjacent
    # target with the fewest hit points is selected; in a tie, the adjacent
    # target with the fewest hit points which is first in reading order
    # is selected.
    # 
    # The unit deals damage equal to its attack power to the selected
    # target, reducing its hit points by that amount. If this reduces its
    # hit points to 0 or fewer, the selected target dies: its square
    # becomes . and it takes no further turns.
    if not to_attack:
      return
    if _VERBOSE > 1:
      print('  => %s can attack %s' % (this, ','.join([str(u) for u in to_attack])))
    hp = 300
    targ = None
    if _ATTACK_FAVOR_X:
      for nx, ny in [(this.x-1, this.y), (this.x+1, this.y), (this.x,this.y-1), (this.x, this.y+1)]:
        for u in sorted(to_attack):
          if u.x == nx and u.y == ny:
            if (u.hp > 0 and u.hp < hp) or (u.hp == hp and u < targ):
              hp = u.hp
              targ = u
    else:
      for u in sorted(to_attack):
        assert this != u
        if (u.hp > 0 and u.hp < hp) or (u.hp == hp and u < targ):
          hp = u.hp
          targ = u
    targ.hp -= this.power
    if targ.hp <= 0:
      if _VERBOSE > 0:
        print('  ==> kills %s' % targ)
      game.Dead(targ)
    else:
      if _VERBOSE > 2:
        print('  ==> does %d points against %s now at %d' % (this.power, targ, targ.hp))


class Game(object):

  WALL = '#'
  ELF = 'E'
  GOBLIN = 'G'
  OPEN = '.'

  def __init__(this):
    this.gen = 0
    this.width = 0
    this.height = 0
    this.rows = []
    this.units = []
    this.distances = {}
    this.unit_locations = {}
    this.turn_limit = 10
    this.to_print = []

  def Add(this, text):
    this.rows.append([c for c in text.strip()])
    this.width = max(this.width, len(text))
    for x in range(len(text.strip())):
      c = text[x]
      if c == Game.ELF or c == Game.GOBLIN:
        u = Unit(c, x, this.height)
        this.units.append(u)
        this.unit_locations[(x, this.height)] = u
    this.height += 1


  def Get(this, x, y):
    return this.rows[y][x]

  def Print(this):
    print('After %d:' % this.gen)
    for y in range(this.height):
      row = this.rows[y]
      hit_points = ''
      for x in range(len(row)):
        u = this.unit_locations.get((x,y))
        if u:
          hit_points += ' %s(%d)' % (u.kind, u.hp)
      print('%s%s' % (''.join(row), hit_points))

  def Flood(this, from_x, from_y, target_kind):
    #if this.distances.get(from_y*this.width + from_x):
    #cached = this.distances.get((from_x, from_y))
    #if cached:
    #  if _VERBOSE > 0:
    #    print('Can reuse flood map for %d,%d' % (from_x, from_y))
    #  return cached

    q = Queue.Queue()
    distances = {}
    q.put((from_x, from_y, 0))
    visited = {}
    while not q.empty():
      x, y, dist = q.get()
      # distances[y*this.width + x] = dist
      distances[(x, y)] = dist
      visited[(x, y)] = 1
      msg = 'Flood  %d,%d d:%d size:%d, add:' % (x, y, dist, q.qsize())
      for nx, ny in [(x, y-1), (x-1, y), (x+1,y), (x, y+1)]:
        if visited.get((nx, ny)):
          continue
        visited[(nx, ny)] = 1
        what = this.Get(nx, ny)
        if what == Game.WALL:
          continue
        if distances.get((nx, ny)) == None:
          if what == Game.OPEN or what == target_kind: 
            q.put((nx, ny, dist+1))
            msg += ' %d,%d' % (nx, ny)
      # print(msg)
    if _VERBOSE > 4:
      print('flood from %d,%d => %s' % (from_x, from_y, distances))
    # this.distances[(from_x, from_y)] = distances
    return distances

  def MoveUnit(this, unit, x, y):
    this.rows[unit.y][unit.x] = Game.OPEN
    del this.unit_locations[(unit.x, unit.y)]
    unit.x = x
    unit.y = y
    this.rows[unit.y][unit.x] = unit.kind
    this.unit_locations[(unit.x, unit.y)] = unit

  def Dead(this, unit):
    this.rows[unit.y][unit.x] = Game.OPEN
    del this.unit_locations[(unit.x, unit.y)]
    this.units = [u for u in this.units if u != unit and u.hp > 0]

  def IsOver(this):
    left = {
        Game.ELF: 0,
        Game.GOBLIN: 0,
    }
    for u in this.units:
      if u.hp > 0:
        left[u.kind] += 1
    if left[Game.ELF] == 0 or left[Game.GOBLIN] == 0:
      return True
    return False

  def Turn(this):
    this.gen += 1
    print('= turn %d' % this.gen)
    this.units = sorted([u for u in this.units if u.hp > 0])
    for unit in list(this.units):
      if _VERBOSE > 0:
        print('= Moving %s' % unit)
      # Move
      if unit.hp <= 0:
        continue
      if this.IsOver():
        return False
      to_attack = unit.Move(this)
      unit.Attack(this, to_attack) 
    this.last_full = this.gen
    return True


#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

def Load(inp):
  game = Game()
  done_with_board = False
  for line in inp:
    line = line.strip()
    if not line:
      continue
    if line.startswith('limit'):
      game.turn_limit = int(line[7:])
    elif line.startswith('='):
       done_with_board = True
    elif line.startswith('After '):
       game.to_print.append(int(''.join([d for d in line[6:] if d.isdigit()])))
    else:
      if not done_with_board:
        game.Add(line)
  return game


# stop on first crash
def part1(game, verbose):
  for i in range(game.turn_limit+1):
    if i in game.to_print:
      game.Print()
    if not game.Turn() or game.IsOver():
      game.Print()
      hp = sum([u.hp for u in game.units])
      print('Done: %d, hp=%d, score=%d' % (game.last_full, hp, hp * (game.last_full)))
      break

def part2(game, elf_power, verbose):
  n_elfs = 0
  for u in game.units:
    if u.kind == Game.ELF:
      n_elfs += 1
      u.power = elf_power
  part1(game, verbose) 
  after_elfs = 0
  for u in game.units:
    if u.kind == Game.ELF:
      after_elfs += 1
  if after_elfs < n_elfs:
    print('FAIL: killed elves')


if __name__ == '__main__':
  verbose = False
  iarg = 1
  do_part2 = False
  while sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      verbose = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      do_part2 = True
      iarg += 1

  with open(sys.argv[iarg]) as inp:
    puzzle = Load(inp)

  if do_part2:
    part2(puzzle, int(sys.argv[iarg+1]), verbose)
  else:
    part1(puzzle, verbose)

"""
Each of the Goblins has open, adjacent squares which are in range
(marked with a ? on the map).  Of those squares, four are reachable
(marked @); the other two (on the right) would require moving through
a wall or unit to reach.  Three of these reachable squares are
nearest, requiring the fewest steps (only 2) to reach (marked !).
Of those, the square which is first in reading order is chosen (+).

The unit then takes a single step toward the chosen square along
the shortest path to that square. If multiple steps would put the
unit equally closer to its destination, the unit chooses the step
which is first in reading order. (This requires knowing when there
is more than one shortest path so that you can consider the first
step of each such path.) For example:

In range:     Nearest:      Chosen:       Distance:     Step:
#######       #######       #######       #######       #######
#.E...#       #.E...#       #.E...#       #4E212#       #..E..#
#...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
#..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
#######       #######       #######       #######       #######
The Elf sees three squares in range of a target (?), two of which
are nearest (!), and so the first in reading order is chosen (+).
Under "Distance", each open square is marked with its distance from
the destination square; the two squares to which the Elf could move
on this turn (down and to the right) are both equally good moves
and would leave the Elf 2 steps from being in range of the Goblin.
Because the step which is first in reading order is chosen, the Elf
moves right one square.

Here's a larger example of movement:

Initially:
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

After 1 round:
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########

After 2 rounds:
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########

After 3 rounds:
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########
Once the Goblins and Elf reach the positions above, they all are
either in range of a target or cannot find any square in range of
a target, and so none of the units can move until a unit dies.

After moving (or if the unit began its turn in range of a target),
the unit attacks.


Each unit, either Goblin or Elf, has 3 attack power and starts with
200 hit points.

For example, suppose the only Elf is about to attack:

       HP:            HP:
G....  9       G....  9  
..G..  4       ..G..  4  
..EG.  2  -->  ..E..     
..G..  2       ..G..  2  
...G.  1       ...G.  1  
The "HP" column shows the hit points of the Goblin to the left in
the corresponding row. The Elf is in range of three targets: the
Goblin above it (with 4 hit points), the Goblin to its right (with
2 hit points), and the Goblin below it (also with 2 hit points).
Because three targets are in range, the ones with the lowest hit
points are selected: the two Goblins with 2 hit points each (one
to the right of the Elf and one below the Elf). Of those, the Goblin
first in reading order (the one to the right of the Elf) is selected.
The selected Goblin's hit points (2) are reduced by the Elf's attack
power (3), reducing its hit points to -1, killing it.

After attacking, the unit's turn ends. Regardless of how the unit's
turn ends, the next unit in the round takes its turn. If all units
have taken turns in this round, the round ends, and a new round
begins.

The Elves look quite outnumbered. You need to determine the outcome
of the battle: the number of full rounds that were completed (not
counting the round in which combat ends) multiplied by the sum of
the hit points of all remaining units at the moment combat ends.
(Combat only ends when a unit finds no targets during its turn.)

Below is an entire sample combat. Next to each map, each row's
units' hit points are listed from left to right.

Initially:
#######   
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#   
#######   

After 1 round:
#######   
#..G..#   G(200)
#...EG#   E(197), G(197)
#.#G#G#   G(200), G(197)
#...#E#   E(197)
#.....#   
#######   

After 2 rounds:
#######   
#...G.#   G(200)
#..GEG#   G(200), E(188), G(194)
#.#.#G#   G(194)
#...#E#   E(194)
#.....#   
#######   

Combat ensues; eventually, the top Elf dies:

After 23 rounds:
#######   
#...G.#   G(200)
#..G.G#   G(200), G(131)
#.#.#G#   G(131)
#...#E#   E(131)
#.....#   
#######   

After 24 rounds:
#######   
#..G..#   G(200)
#...G.#   G(131)
#.#G#G#   G(200), G(128)
#...#E#   E(128)
#.....#   
#######   

After 25 rounds:
#######   
#.G...#   G(200)
#..G..#   G(131)
#.#.#G#   G(125)
#..G#E#   G(200), E(125)
#.....#   
#######   

After 26 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(122)
#...#E#   E(122)
#..G..#   G(200)
#######   

After 27 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(119)
#...#E#   E(119)
#...G.#   G(200)
#######   

After 28 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(116)
#...#E#   E(113)
#....G#   G(200)
#######   

More combat ensues; eventually, the bottom Elf dies:

After 47 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(59)
#...#.#   
#....G#   G(200)
#######   
Before the 48th round can finish, the top-left Goblin finds that
there are no targets remaining, and so combat ends. So, the number
of full rounds that were completed is 47, and the sum of the hit
points of all remaining units is 200+131+59+200 = 590. From these,
the outcome of the battle is 47 * 590 = 27730.

Here are a few example summarized combats:

#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 982 total hit points left
Outcome: 37 * 982 = 36334
#######       #######   
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#   
#######       #######   

Combat ends after 46 full rounds
Elves win with 859 total hit points left
Outcome: 46 * 859 = 39514
#######       #######   
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#   
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######   

Combat ends after 35 full rounds
Goblins win with 793 total hit points left
Outcome: 35 * 793 = 27755
#######       #######   
#.E...#       #.....#   
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#   
#E#G#G#       #.#.#.#   
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######   

Combat ends after 54 full rounds
Goblins win with 536 total hit points left
Outcome: 54 * 536 = 28944
#########       #########   
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#   
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740

What is the outcome of the combat described in your puzzle input?
"""
