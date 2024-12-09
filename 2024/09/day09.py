#!/usr/bin/env python3
"AOC 2023: day 09"

from collections import defaultdict
import copy

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

  def do_line(self, line):
    # called for each line of input
    pass

  def build_map(self):
    # called after all input is read
    self.files = [int(c) for c in self.all_input[0][::2]]
    self.free  = [int(c) for c in self.all_input[0][1::2]]
    self.free.append(0)
    if self.doing_sample:
      print('file sizes', self.files)
      print('free sizes', self.free)

    # compute starts of used and free spots
    self.n_files = len(self.files)
    self.file_start = [0] * self.n_files 
    self.free_start = [0] * self.n_files 
    at = 0
    self.total_used = 0
    self.total_free = 0
    for i in range(self.n_files):
      self.file_start[i] = at
      at += self.files[i]
      self.total_used += self.files[i]
      self.free_start[i] = at
      at += self.free[i]
      self.total_free += self.free[i]
    if self.doing_sample:
      print('file starts', self.file_start)
      print('free starts', self.free_start)
    print("Total: %d used, %d free" % (self.total_used, self.total_free))


  def part1(self):
    print('===== Start part 1')
    self.build_map()
    unmoved_blocks = copy.copy(self.files)
    block = 0  # block we are indexing
    chk = 0
    cur_file = 0
    cur_last = self.n_files - 1
    print("cur last file", cur_last)
    while block < self.total_used:
      # for i in range(self.files[cur_file]):
      for i in range(unmoved_blocks[cur_file]):
        chk += block * cur_file
        if self.doing_sample:
          print('block %d, file %d: sum %d   file_size:%d' % (block, cur_file, chk, self.files[cur_file]))
        block += 1
        if block >= self.total_used:
          break
      if block >= self.total_used:
        break
      for i in range(self.free[cur_file]):  # there is a free per file
        if unmoved_blocks[cur_last] <= 0:
          cur_last -= 1
        unmoved_blocks[cur_last] -= 1
        chk += block * cur_last
        if self.doing_sample:
          print('block %d, file %d: sum %d' % (block, cur_last, chk))
        block += 1
        if block >= self.total_used:
          break
      cur_file += 1

    return chk


  def part2(self):
    print('===== Start part 2')
    self.reset()
    self.build_map()

    # Move them
    cur_last = self.n_files - 1
    while cur_last > 0:
      want = self.files[cur_last]
      moved = False
      for i_free in range(len(self.free)):
        size = self.free[i_free]
        if size >= want and self.free_start[i_free] < self.file_start[cur_last]:
          self.file_start[cur_last] = self.free_start[i_free]
          if self.doing_sample:
            print('Moved file %d for %d to %d' % (cur_last, want, self.free_start[i_free]))
          self.free[i_free] -= want
          self.free_start[i_free] += want
          moved = True
          break
      cur_last -= 1

    chk = 0
    for file_i in range(self.n_files):
      block = self.file_start[file_i]
      # print('block %d, file %d: sum %d   file_size:%d' % (block, file_i, chk, self.files[file_i]))
      for i in range(self.files[file_i]):
        chk += block * file_i
        block += 1

    return chk


day09.sample_test("""
2333133121414131402
""", expect1=1928, expect2=2858)


if __name__ == '__main__':
  # 8446022420670 too high
  day09.run_and_check('input.txt', expect1=6225730762521, expect2=6250605700557)
