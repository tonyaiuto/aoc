from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys

"""
You talk to the Elves while you wait for your navigation system to
initialize. To pass the time, they introduce you to their favorite
marble game.

The Elves play this game by taking turns arranging the marbles in
a circle according to very particular rules. The marbles are numbered
starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point,
while it contains only a single marble, it is still a circle: the
marble is both clockwise from itself and counter-clockwise from
itself. This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining
marble into the circle between the marbles that are 1 and 2 marbles
clockwise of the current marble. (When the circle is large enough,
this means that there is one marble between the marble that was
just placed and the current marble.) The marble that was just placed
then becomes the current marble.

However, if the marble that is about to be placed has a number which
is a multiple of 23, something entirely different happens. First,
the current player keeps the marble they would have placed, adding
it to their score. In addition, the marble 7 marbles counter-clockwise
from the current marble is removed from the circle and also added
to the current player's score. The marble located immediately
clockwise of the marble that was removed becomes the new current
marble.

For example, suppose there are 9 players. After the marble with
value 0 is placed in the middle, each player (shown in square
brackets) takes a turn. The result of each of those turns would
produce circles of marbles like this, where clockwise is to the
right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1 
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3 
[5]  0  4  2 (5) 1  3 
[6]  0  4  2  5  1 (6) 3 
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7 
[9]  0  8  4 (9) 2  5  1  6  3  7 
[1]  0  8  4  9  2(10) 5  1  6  3  7 
[2]  0  8  4  9  2 10  5(11) 1  6  3  7 
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7 
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7 
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7 
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15 
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15 
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15 
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15 
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15 
[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15 
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15 
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15

The goal is to be the player with the highest score after the last marble is used up. Assuming the example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept marble 23 and removed marble 9, while no other player got any points in this very short example game).

Here are a few more examples:

10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305

What is the winning Elf's score?
"""

class Cell(object):
  def __init__(this, v, prev, next):
    this.value = v
    this.prev = prev
    this.next = next
    if this.prev:
      this.prev.next = this
    if this.next:
      this.next.prev = this

  def __str__(this):
    return '(%d, %s)' % (this.value, this.next)


class Marbles(object):

  def __init__(this, nplayers, nrounds):
    this.nplayers = nplayers
    this.nrounds = nrounds
    this.scores = [0] * this.nplayers
    this.board = Cell(0, None, None)
    this.board.prev = this.board
    this.board.next = this.board
    this.len_board = 1
    this.cur = this.board
    this.turn = -1
    this.next = 1

  def __str__(this):
    ret = '[%d]' % (this.turn + 1)
    c = this.board
    for i in range(this.len_board):
      if c == this.cur:
        ret += ' (%d)' % c.value
      else:
        ret += ' %d' % c.value
      c = c.next
    return ret

  def Turn(this):
    this.turn = (this.turn + 1) % this.nplayers
    if this.next % 23 == 0:
      drop = this.cur
      for i in range(7):
        drop = drop.prev
      this.scores[this.turn] += this.next + drop.value
      drop.prev.next = drop.next
      drop.next.prev = drop.prev
      if this.board == drop:
        this.board = drop.next
      this.cur = drop.next
      this.len_board -= 1
    else:
      c = this.cur.next
      #if c == None:
      #  c = this.board
      this.cur = c.next = Cell(this.next, c, c.next)
      this.len_board += 1
    this.next += 1

  def results(this):
    m = 0
    i_m = 0
    for i in range(this.nplayers):
      if this.scores[i] > m:
        i_m = i
        m = this.scores[i]
    print('%d players; last=%d points, high score is %d' % (
        this.nplayers, this.nrounds, m))


def part1():
  game = Marbles(9, 25)
  print(game)
  for i in range(25):
    game.Turn()
    print(game)
  game.results()
  game = Marbles(30, 5807)
  for i in range(game.nrounds):
    game.Turn()
  game.results()
  game = Marbles(419, 71052)
  for i in range(game.nrounds):
    game.Turn()
  game.results()

def part2():
  game = Marbles(419, 7105200)
  for i in range(game.nrounds):
    game.Turn()
  game.results()


if __name__ == '__main__':
  verbose = False
  iarg = 1
  if len(sys.argv) > 1 and sys.argv[iarg] == '-v':
    verbose = True
    iarg += 1
  part1()
  part2()
