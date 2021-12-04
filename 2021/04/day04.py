"AOC 2021: day 04"

from collections import defaultdict
import math

from tools import aoc


class Board1(object):

  def __init__(self, lines, number=None):
    self.number = number
    self.rows = []
    for row in range(5):
      self.rows.append([int(n) for n in lines[row].replace('  ', ' ').split()])

  def __str__(self):
    return str(self)

  def print(self):
    print('Board:', self.number)
    for row in range(5):
      print(' '.join(['%2d' % n for n in self.rows[row]]))

  def score(self):
    score = 0
    for row in range(5):
      for col in range(5):
        if self.rows[row][col] != 0:
          score += self.rows[row][col]
    return score

  def mark(self, n):
    # returns True if the mark is a bingo
    found = -1
    for row in range(5):
      for col in range(5):
        if self.rows[row][col] == n:
          self.rows[row][col] = 0
          #print('..... found', n, 'at', row, col)
          #self.print()
          if sum(self.rows[row]) == 0:
            return True
          found = col
          break
      if found >= 0:
        for row in range(5):
          if self.rows[row][found] != 0:
            return False
        return True
    return False

  def is_won(self):
    for row in range(5):
      if sum(self.rows[row]) == 0:
        return True
    for col in range(5):
      won = True
      for row in range(5):
        if self.rows[row][col] != 0:
          won = False
          break
      if won:
        return True
    return False

class Board(object):

  def __init__(self, lines, number=None):
    self.number = number
    self.rows = []
    for row in range(5):
      self.rows.append([int(n) for n in lines[row].replace('  ', ' ').split()])
    self.pos = {}
    self.row_sum = [0] * 5
    self.col_sum = [0] * 5
    for row in range(5):
      for col in range(5):
        n = self.rows[row][col]
        self.pos[n] = (row, col)
        self.row_sum[row] += n
        self.col_sum[col] += n

  def __str__(self):
    return str(self)

  def print(self):
    print('Board:', self.number)
    for row in range(5):
      print(' '.join(['%2d' % n for n in self.rows[row]]))

  def score(self):
    return (sum(self.row_sum) + sum(self.col_sum)) // 2

  def mark(self, n):
    # returns True if the mark is a bingo
    rc = self.pos.get(n)
    if not rc:
      return False
    row = rc[0]
    col = rc[1]
    self.row_sum[row] -= n
    self.col_sum[col] -= n
    return self.row_sum[row] == 0 or self.col_sum[col] == 0


class day04(aoc.aoc):

  def __init__(self):
    super(day04, self).__init__(
        reader_params={
            'by_group': True,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    pass

  def post_load(self):
    # called after all input is read
    self.boards = []
    i = 0
    for g in self.reader.all:
      if i == 0:
        self.tosses = [int(n) for n in g[0].split(',')]
        # print(self.tosses)
      else:
        b = Board(g, number=i)
        self.boards.append(b)
        # b.print()
      i += 1

  def part1(self):
    print('===== Start part 1')
    self.reset()

    i = 0
    for t in self.tosses:
      i += 1
      # print('turn', i, 'n', t)
      for b in self.boards:
        bingo = b.mark(t)
        if bingo:
          print('bingo')
          b.print()
          score = b.score()
          return score * t
    return 0


  def part2(self):
    print('===== Start part 2')

    i = 0
    solved = []
    blast = None
    for t in self.tosses:
      i += 1
      # print('turn', i, 'n', t)
      for b in self.boards:
        if b.number in solved:
          continue
        bingo = b.mark(t)
        if bingo:
          # print('bingo')
          # b.print()
          solved.append(b.number)
          blast = b
      if len(solved) == len(self.boards):
        score = blast.score() * t
        break
    return score


day04.sample_test("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""", expect1=4512, expect2=1924)


if __name__ == '__main__':
  day04.run_and_check('input.txt', expect1=None, expect2=None)
