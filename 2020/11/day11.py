"AOC 2020: day 11"

from collections import defaultdict
import traceback

from tools import reader


def sample_test(s, expect, gens):
  puzz = day11()
  puzz.load_str(s)
  res = puzz.part1()
  print(puzz.result1)
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  p2 = day11()
  p2.load_str(s)
  res = p2.part2(expect_gens=gens)


def main(input):
  puzz = day11()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)

  puzz = day11()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)


class Foo(object):

  def __init__(self):
    pass


  def __str__(self):
    return str(self)



class day11(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.rows = []
    self.ncols = 0
    self.gen = 0
    self.trace = False

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    self.ncols = max(self.ncols, len(line)+2)
    if line:
      self.rows.append('.%s.' % line)

  def post_load(self):
    self.nrows = len(self.rows)
    self.rows = ['.' * self.ncols] + self.rows + ['.' * self.ncols]
    self.nrows = len(self.rows)
    self.gen = 0
    self.print()

  def print(self):
    print('=== gen', self.gen)
    for row in self.rows:
      print('  ', row)

  def run_gen(self):
    self.gen += 1
    match = True
    nrows = [self.rows[0]]
    for row in range(1, len(self.rows)):
      rr = self.rows[row]
      new_row = '.'
      for col in range(1, len(rr)-1):
        seat = rr[col]
        if seat != '.':
          n = self.ncount(row, col)
          if n == 0 and seat == 'L':
            seat = '#'
          elif n >= 4 and seat == '#':
            seat = 'L'
        new_row += seat
      new_row += '.'

      if rr != new_row:
        match = False
        # print('DIFF ', rr, new_row)
      nrows.append(new_row)
    self.rows = nrows
    return match

  def check_match(self, expected):
    match = True
    e = expected.split('\n')
    for i in range(len(e)):
      if e[i] != self.rows[i+1][1:-1]:
        print('fail row %2d' % i, e[i], self.rows[i+1][1:-1])
        match = False


  def ncount(self, row, col):
    ret = 0
    cix = (-1, 0, 1)
    if row >= 1:
      for ci in (-1,0,1):
        if self.rows[row-1][col+ci] == '#':
          ret += 1
    for ci in (-1, 1):
      if self.rows[row][col+ci] == '#':
        ret += 1
    if row < len(self.rows) - 1:
      for ci in (-1,0,1):
        if self.rows[row+1][col+ci] == '#':
          ret += 1
    return ret

  def nocc(self):
    print("Count occupied")
    occ = 0
    for row in self.rows:
      print('occ:', row)
      for seat in row:
        if seat == '#':
          occ += 1
    return occ


  def part1(self):
    print('========= start part 1===========')
    self.result1 = None
    while self.gen < 100:
      if self.gen % 10 == 0:
        self.print()
      if self.run_gen():
        print("======================== match")
        self.print()
        break
    self.result1 = self.nocc()
    return self.result1


  def fill_diags(self, row, col, vc):

    def inc_end(ri, ci):
      nonlocal trace

      seat = self.rows[ri][ci]
      if trace:
        print('  inc_end:', ri, ci, seat)
      if ri < 1 or ci < 1:
        if trace:
          print('  inc_end: off left top edge')
        return True
      if ri >= self.nrows - 1 or ci >= self.ncols - 1:
        if trace:
          print('  inc_end: off right bottom edge')
        return True
      if seat in ('L', '#'):
        vc[ri][ci] += 1
        if trace:
          print('  inc_end: INC to', vc[ri][ci])
      if ri == 1 and ci == 1:
        assert vc[ri][ci] <= 3
      return seat in ('L', '#')

    trace = False
    if row == 2 and col == 2:
      trace = 2

    for i in range(1, max(self.nrows, self.ncols)):
      if inc_end(row - i, col - i):
         break
    for i in range(1, max(self.nrows, self.ncols)):
      if inc_end(row - i, col + i):
         break
    for i in range(1, max(self.nrows, self.ncols)):
      if inc_end(row + i, col - i):
         break
    for i in range(1, max(self.nrows, self.ncols)):
      if inc_end(row + i, col + i):
         break


  def run_gen2(self):
    self.gen += 1
    self.nrows = len(self.rows)
    nrows = [self.rows[0]]
    upvis = [False] * self.ncols
    downvis = [False] * self.ncols
    vc = []
    for i in range(self.nrows):
      vc.append([0] * self.ncols)

    vc11 = -1

    # diag_l_up = [False] * self.ncols
    # diag_r_up = [False] * self.ncols
    # diag_l_down = [False] * self.ncols
    # diag_r_down = [False] * self.ncols
    for row in range(1, self.nrows-1):
      rr = self.rows[row]
      down_row = self.nrows - 1 - row
      assert down_row < self.nrows - 1
      dr = self.rows[down_row]

      lvis = False
      rvis = False
      # diag_l_up = diag_l_up[1:] + [False]
      # diag_r_up = [False] + diag_r_up[0:-1]
      # diag_l_down = diag_l_down[1:] + [False]
      # diag_r_down = [False] + diag_r_down[0:-1]
      # assert len(diag_l_up) == len(diag_r_up)
      if self.trace:
        x = ''
        for col in range(self.ncols):
          x += 'l' if diag_l_up[col] else ' '
          x += 'u' if upvis[col] else ' '
          x += 'r ' if diag_r_up[col] else '  '
        print('#')
        print('  u %2d:' % row, x)
        print('  < %2d:' % row, '  '.join('%2d' % x for x in vc[row]))
        x = ''
        for col in range(self.ncols):
          x += 'l' if diag_l_down[col] else ' '
          x += 'd' if downvis[col] else ' '
          x += 'r ' if diag_r_down[col] else '  '
        print('  d %2d:' % row, x)


      def check():
        nonlocal vc11
        if vc11 != vc[1][1]:
          print('1, 1, change from', vc11, 'to', vc[1][1])
          print(traceback.format_stack())
          vc11 = vc[1][1]

        if False:
          if vc[4][5] != 0:
            print('XX row', row, down_row, 'col', col, rcol)
            print('   cell=', self.rows[4][5])
          assert vc[4][5] == 0

      for col in range(1, self.ncols-1):
        rcol = self.ncols - 1 - col
        lseat = rr[col]
        rseat = rr[rcol]
        dseat = dr[col]

        if self.trace and row == 4:
          print('%s @%d %c    %c @%d %s' % (lvis, col, lseat,     rseat, rcol, rvis))
        if lseat in ('L', '#'):
          if lvis:
            vc[row][col] += 1
          check()
        if rseat in ('L', '#'):
          if rvis:
            vc[row][rcol] += 1
          check()

        if lseat in ('L', '#'):
          if upvis[col]:
            vc[row][col] += 1
          check()
          """
          if diag_l_up[col]:
            vc[row][col] += 1
          check()
          if diag_r_up[col]:
            vc[row][col] += 1
          check()
          """

        if dseat in ('L', '#'):
          if downvis[col]:
            vc[down_row][col] += 1
          check()
          """
          #if diag_l_down[col]:
          #  vc[down_row][col] += 1
          #check()
          #if diag_r_down[col]:
          #  vc[down_row][col] += 1
          #check()
          """

        if lseat == '#':
          lvis = True
          upvis[col] = True
        elif lseat == 'L':
          lvis = False
          upvis[col] = False
        if rseat == '#':
          rvis = True
        elif rseat == 'L':
          rvis = False

        if lseat == '#':
          """
          #diag_l_up[col] = True
          #diag_r_up[col] = True
          """
          self.fill_diags(row, col, vc)

        if dseat == '#':
          downvis[col] = True
        elif dseat == 'L':
          downvis[col] = False
          """
          #diag_l_down[col] = True
          #diag_r_down[col] = True
          """

      if self.trace:
        print('  X %2d:' % row, ' '.join('%2d' % x for x in vc[row]))

    if True or self.trace:
      print("  vc====")
      for row in range(1, self.nrows):
        print('   %2d:' % row, ' '.join('%2d' % x for x in vc[row]))
      print("  end vc====")
    match = True
    for row in range(1, self.nrows-1):
      rr = self.rows[row]
      new_row = '.'
      for col in range(1, self.ncols):
        seat = rr[col]
        if seat != '.':
          n = vc[row][col]
          if n == 0 and seat == 'L':
            seat = '#'
          elif n >= 5 and seat == '#':
            seat = 'L'
        new_row += seat
      if rr != new_row:
        match = False
      nrows.append(new_row)
    nrows.append(self.rows[0])
    self.rows = nrows

    return match


  def part2(self, expect_gens=None):
    print('========= start part 2===========')
    self.result2 = None
    while self.gen < 1000:
      if self.gen % 10 == 0:
        self.print()
      if self.run_gen2():
        print("======================== match")
        self.print()
        break
      if expect_gens and len(expect_gens) > self.gen:
        self.check_match(expect_gens[self.gen -1])

    self.result2 = self.nocc()
    print('part2', self.result2)
    return self.result2

def gen2(s):
  puzz = day11()
  puzz.load_str(s)
  puzz.run_gen2()
  puzz.print()
  print(puzz.result2)


sample_test("""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""", 37, gens=["""#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""", """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#""", """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#"""])


gen2("""
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
""")

if __name__ == '__main__':
  main('input.txt')
  pass
