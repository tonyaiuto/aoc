"AOC 2021: day 09"

from tools import aoc


class day09(aoc.aoc):

  def __init__(self):
    super(day09, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.grid = [0]
    self.nrows = 0
    self.ncols = 0

  def do_line(self, line):
    # called for each line of input
    self.nrows += 1
    row = [11]
    row.extend([int(h) for h in line])
    row.append(11)
    self.grid.append(row)
    self.ncols = max(self.ncols, len(line))

  def post_load(self):
    # called after all input is read
    self.grid[0] = [11] * (self.ncols + 2)
    self.grid.append([11] * (self.ncols + 2))
    print('shape', self.nrows, self.ncols)
    if self.trace_sample:
      print(self.grid)

  def n4(self, r, c):
    return (self.grid[r-1][c], self.grid[r+1][c], self.grid[r][c-1], self.grid[r][c+1])

  def part1(self):
    print('===== Start part 1')

    risk = 0
    self.minima = []
    for row in range(1, self.nrows+1):
      for col in range(1, self.ncols+1):
        if self.grid[row][col] < min(self.n4(row, col)):
          height = self.grid[row][col]
          risk += height + 1
          self.minima.append((row,col))
          if self.trace_sample:
            print('minima at ', row, col, 'is', height)
    return risk

  def part2(self):
    print('===== Start part 2')
    if self.trace_sample:
      print(self.minima)

    sizes = []
    for r, c in self.minima:
      basin = set()
      self.expand_basin(basin, r, c)
      if self.trace_sample:
        print(basin) 
        print('basin size', len(basin))
      sizes.append(len(basin))
 
    b = sorted(sizes)[-3:]
    print(b)
    return b[0] * b[1] * b[2]

  def expand_basin(self, basin, r, c):
    basin.add(r*1000+c)
    to_visit = [(r+1,c), (r-1, c), (r, c+1), (r,c-1)]
    for r,c in to_visit:
      if r*1000+c in basin:
        continue
      if self.grid[r][c] >= 9:
        continue
      self.expand_basin(basin, r, c)

day09.sample_test("""
2199943210
3987894921
9856789892
8767896789
9899965678
""", expect1=15, expect2=1134, recreate=False)


if __name__ == '__main__':
  day09.run_and_check('input.txt', expect1=603, expect2=786780, recreate=False)
