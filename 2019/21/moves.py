#!/usr/bin/env python3



def b(suffix):
  yield '#' + suffix
  yield '.' + suffix


def x():
  states = ['#', '.']
  for a in ['#']:
    for b in states:
      for c in states:
        for d in '#':
          for e in states:
            for f in states:
              for g in states:
                for h in states:
                  for i in states:
                    s = a+b+c+d+e+f+g+h+i
                    jump = 'hold'
                    if a == '.':
                      jump = 'jump'
                    elif e == '.':
                      jump = 'no'

                    print(s, ' ', jump)

#  ###......

x()

"""


part1

 abcd
b....	dead
#...#	jump	^c & d
#..#.	dead
#..##	jump
#.#..	dead
#.#.#	jump
#.##.	dead
#.###	jump

##...   hold
##..#   jump
##.#.   hold
##.##   jump
###..   hold
###.#   jump
####.	hold
#####	hold

 .@abcd........
#####.#..########

T
^a & ^b & ^c & d
^a & ^b &  c & d
^a &  b & ^c & d
^a &  b &  c & d
 a & ^b &  ? & d

LAST
AND D J

^a 
^a
^a
^a
 a & ^b


not b j
and a j  a & ^b
not c t
and a t
and b t
or  t j
NOT A T
OR  T J
AND D J

-----------
part2


##..##   jump
##.###   jump
###.##   jump

##..#.  hold
##.##.  hold
###.#.  hold

##...#  hold
##.#.#  hold
###..#  hold
####.#	hold
######	hold

##....	hold
##.#..	hold
###...	hold
####..	hold
#####.	hold

b.....	dead
#...##	jump
#...#.	dead
#..#..	dead
#..##.	jump
#.#...	dead
#.#.#.	jump
#.##..	dead
#.###.	jump
##....	hold
##..#.	jump
##.#..	hold
##.##.	jump
###..r	hold
###.#	jump
####.	hold
#####	hold

abcdefjhi
???#

#########
########.
#######.#
#######..
######.##
######.#.
######..#
######...
#####.###
#####.##.
#####.#.#
#####.#..
#####..##
#####..#.
#####...#
#####....
####.####
####.###.
####.##.#
####.##..
####.#.##
####.#.#.
####.#..#
####.#...
####..###
####..##.
####..#.#
####..#..
####...##
####...#.
####....#
####.....
###.#####
###.####.
###.###.#
###.###..
###.##.##
###.##.#.
###.##..#
###.##...
###.#.###
###.#.##.
###.#.#.#
###.#.#..
###.#..##
###.#..#.
###.#...#
###.#....
###..####
###..###.
###..##.#
###..##..
###..#.##
###..#.#.
###..#..#
###..#...
###...###
###...##.
###...#.#
###...#..
###....##
###....#.
###.....#
###......
##.######
##.#####.
##.####.#
##.####..
##.###.##
##.###.#.
##.###..#
##.###...
##.##.###
##.##.##.
##.##.#.#
##.##.#..
##.##..##
##.##..#.
##.##...#
##.##....
##.#.####
##.#.###.
##.#.##.#
##.#.##..
##.#.#.##
##.#.#.#.
##.#.#..#
##.#.#...
##.#..###
##.#..##.
##.#..#.#
##.#..#..
##.#...##
##.#...#.
##.#....#
##.#.....
##..#####
##..####.
##..###.#
##..###..
##..##.##
##..##.#.
##..##..#
##..##...
##..#.###
##..#.##.
##..#.#.#
##..#.#..
##..#..##
##..#..#.
##..#...#
##..#....
##...####
##...###.
##...##.#
##...##..
##...#.##
##...#.#.
##...#..#
##...#...
##....###
##....##.
##....#.#
##....#..
##.....##
##.....#.
##......#
##.......
#.#######
#.######.
#.#####.#
#.#####..
#.####.##
#.####.#.
#.####..#
#.####...
#.###.###
#.###.##.
#.###.#.#
#.###.#..
#.###..##
#.###..#.
#.###...#
#.###....
#.##.####
#.##.###.
#.##.##.#
#.##.##..
#.##.#.##
#.##.#.#.
#.##.#..#
#.##.#...
#.##..###
#.##..##.
#.##..#.#
#.##..#..
#.##...##
#.##...#.
#.##....#
#.##.....
#.#.#####
#.#.####.
#.#.###.#
#.#.###..
#.#.##.##
#.#.##.#.
#.#.##..#
#.#.##...
#.#.#.###
#.#.#.##.
#.#.#.#.#
#.#.#.#..
#.#.#..##
#.#.#..#.
#.#.#...#
#.#.#....
#.#..####
#.#..###.
#.#..##.#
#.#..##..
#.#..#.##
#.#..#.#.
#.#..#..#
#.#..#...
#.#...###
#.#...##.
#.#...#.#
#.#...#..
#.#....##
#.#....#.
#.#.....#
#.#......
#..######
#..#####.
#..####.#
#..####..
#..###.##
#..###.#.
#..###..#
#..###...
#..##.###
#..##.##.
#..##.#.#
#..##.#..
#..##..##
#..##..#.
#..##...#
#..##....
#..#.####
#..#.###.
#..#.##.#
#..#.##..
#..#.#.##
#..#.#.#.
#..#.#..#
#..#.#...
#..#..###
#..#..##.
#..#..#.#
#..#..#..
#..#...##
#..#...#.
#..#....#
#..#.....
#...#####
#...####.
#...###.#
#...###..
#...##.##
#...##.#.
#...##..#
#...##...
#...#.###
#...#.##.
#...#.#.#
#...#.#..
#...#..##
#...#..#.
#...#...#
#...#....
#....####
#....###.
#....##.#
#....##..
#....#.##
#....#.#.
#....#..#
#....#...
#.....###
#.....##.
#.....#.#
#.....#..
#......##
#......#.
#.......#
#........
.########
.#######.
.######.#
.######..
.#####.##
.#####.#.
.#####..#
.#####...
.####.###
.####.##.
.####.#.#
.####.#..
.####..##
.####..#.
.####...#
.####....
.###.####
.###.###.
.###.##.#
.###.##..
.###.#.##
.###.#.#.
.###.#..#
.###.#...
.###..###
.###..##.
.###..#.#
.###..#..
.###...##
.###...#.
.###....#
.###.....
.##.#####
.##.####.
.##.###.#
.##.###..
.##.##.##
.##.##.#.
.##.##..#
.##.##...
.##.#.###
.##.#.##.
.##.#.#.#
.##.#.#..
.##.#..##
.##.#..#.
.##.#...#
.##.#....
.##..####
.##..###.
.##..##.#
.##..##..
.##..#.##
.##..#.#.
.##..#..#
.##..#...
.##...###
.##...##.
.##...#.#
.##...#..
.##....##
.##....#.
.##.....#
.##......
.#.######
.#.#####.
.#.####.#
.#.####..
.#.###.##
.#.###.#.
.#.###..#
.#.###...
.#.##.###
.#.##.##.
.#.##.#.#
.#.##.#..
.#.##..##
.#.##..#.
.#.##...#
.#.##....
.#.#.####
.#.#.###.
.#.#.##.#
.#.#.##..
.#.#.#.##
.#.#.#.#.
.#.#.#..#
.#.#.#...
.#.#..###
.#.#..##.
.#.#..#.#
.#.#..#..
.#.#...##
.#.#...#.
.#.#....#
.#.#.....
.#..#####
.#..####.
.#..###.#
.#..###..
.#..##.##
.#..##.#.
.#..##..#
.#..##...
.#..#.###
.#..#.##.
.#..#.#.#
.#..#.#..
.#..#..##
.#..#..#.
.#..#...#
.#..#....
.#...####
.#...###.
.#...##.#
.#...##..
.#...#.##
.#...#.#.
.#...#..#
.#...#...
.#....###
.#....##.
.#....#.#
.#....#..
.#.....##
.#.....#.
.#......#
.#.......
..#######
..######.
..#####.#
..#####..
..####.##
..####.#.
..####..#
..####...
..###.###
..###.##.
..###.#.#
..###.#..
..###..##
..###..#.
..###...#
..###....
..##.####
..##.###.
..##.##.#
..##.##..
..##.#.##
..##.#.#.
..##.#..#
..##.#...
..##..###
..##..##.
..##..#.#
..##..#..
..##...##
..##...#.
..##....#
..##.....
..#.#####
..#.####.
..#.###.#
..#.###..
..#.##.##
..#.##.#.
..#.##..#
..#.##...
..#.#.###
..#.#.##.
..#.#.#.#
..#.#.#..
..#.#..##
..#.#..#.
..#.#...#
..#.#....
..#..####
..#..###.
..#..##.#
..#..##..
..#..#.##
..#..#.#.
..#..#..#
..#..#...
..#...###
..#...##.
..#...#.#
..#...#..
..#....##
..#....#.
..#.....#
..#......
...######
...#####.
...####.#
...####..
...###.##
...###.#.
...###..#
...###...
...##.###
...##.##.
...##.#.#
...##.#..
...##..##
...##..#.
...##...#
...##....
...#.####
...#.###.
...#.##.#
...#.##..
...#.#.##
...#.#.#.
...#.#..#
...#.#...
...#..###
...#..##.
...#..#.#
...#..#..
...#...##
...#...#.
...#....#
...#.....
....#####
....####.
....###.#
....###..
....##.##
....##.#.
....##..#
....##...
....#.###
....#.##.
....#.#.#
....#.#..
....#..##
....#..#.
....#...#
....#....
.....####
.....###.
.....##.#
.....##..
.....#.##
.....#.#.
.....#..#
.....#...
......###
......##.
......#.#
......#..
.......##
.......#.
........#
.........

"""