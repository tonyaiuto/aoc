#!/usr/bin/env python3
"AOC 2021: day 18"

from collections import defaultdict
import sys

from tools import aoc


class inpstream(object):

  def __init__(self, s):
    self.s = s
    self.pos = 0
    self.push = None

  def next(self):
    if self.push:
      ret = self.push
      self.push = None
    else:
      if self.pos >= len(self.s):
        return None
      ret = self.s[self.pos]
      self.pos += 1
    return ret

  def pushback(self, c):
    self.push = c



class SN(object):

  def __init__(self, parent, n=0):
    self.l = None
    self.r = None
    self.n = n
    self.parent = parent
    pass

  def __str__(self):
    if self.l == None:
      return str(self.n)
    return '[%s,%s]' % (self.l, self.r)

  @property
  def is_number(self):
    return not self.l

  @staticmethod
  def parse(s):
    inp = inpstream(s)
    return SN._parse(inp, None)

  @staticmethod
  def _parse(inp, parent):
    collect_n = False
    expect_comma = False
    
    while True:
      c = inp.next()
      if not c:
        return
      if c == '[':
        ret = SN(parent)
        ret.l = SN._parse(inp, ret)
        # print(' left:', ret.l)
        SN._expect(inp, ',')
        ret.r = SN._parse(inp, ret)
        SN._expect(inp, ']')
        return ret

      if c.isdigit():
         if not collect_n:
           collect_n = True
           expect_comma = True
           n = 0
         n = n * 10 + int(c)
         continue
      else:
        inp.pushback(c)
        if collect_n:
          ret = SN(parent)
          ret.n = n
          return  ret

  @staticmethod
  def _expect(inp, expect_c):
    c = inp.next()
    if expect_c != c:
      print('expected %s, got %s' % (expect_c, c))
      assert expect_c == c
    return

  def magnitude(self):
     if self.l:
       return 3 * self.l.magnitude() + 2 * self.r.magnitude() 
     return self.n

  def reduce(self, one_loop=False):

    while True:
      if not self.check_explode(0):
        if not self.check_split(0):
          return
      if one_loop:
        return

    print('should not reach here ==================')
    return


  def check_explode(self, level):
    if self.is_number:
      return

    if level == 4:
      print('explode me', self, 'in', self.parent)
      assert self.l.is_number
      assert self.r.is_number
      self.add_to_the_left(self.l.n)
      print('     => add left', self.parent.parent.parent)
      self.add_to_the_right(self.r.n)
      print('     => add right', self.parent.parent.parent)
      self.l = None
      self.r = None
      self.n = 0
      print('     => final', self.parent.parent.parent)
      return True

    if self.l.check_explode(level+1):
      return True
    if self.r.check_explode(level+1):
      return True
    return False


  def add_to_the_left(self, n: int):
    """Find rightmost N to the lef of me.

    If I am the RHS of a pair, search down my sibling.
    If I am the LHS of a pair, go up and try again
    """
    cur = self
    i = 0
    while True:
      p = cur.parent
      if not p:
        return False
      i += 1
      assert i < 10
      if cur == p.r:
        if p.l.add_rightmost_down(n):
          return True
      cur = p
    return False

  def add_rightmost_down(self, n):
     if self.is_number:
       self.n += n
       return True
     if self.r.add_rightmost_down(n):
       return True
     if self.l.add_rightmost_down(n):
       return True
     return False

  def add_to_the_right(self, n: int):
    """Find leftmost N to the right of me.

    If I am the LHS of a pair, search down my sibling.
    If I am the RHS of a pair, go up and try again
    """
    cur = self
    while True:
      p = cur.parent
      if not p:
        return False
      if cur == p.l:
        if p.r.add_leftmost_down(n):
          return True
      cur = p
    return False

  def add_leftmost_down(self, n):
     if self.is_number:
       self.n += n
       return True
     if self.l.add_leftmost_down(n):
       return True
     if self.r.add_leftmost_down(n):
       return True
     return False
   
  def check_split(self, level):
    if self.is_number:
      if self.n >= 10:
        self.l = SN(parent=self, n=(self.n // 2))
        self.r = SN(parent=self, n=(self.n - (self.n // 2)))
        self.n = 0
        return True
      return False

    if self.l.check_explode(level + 1):
      return True
    if self.r.check_explode(level + 1):
      return True
    return False

   

class day18(aoc.aoc):

  def __init__(self):
    super(day18, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.exprs = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    e = SN.parse(line)
    if self.trace_sample:
      print(e)
    e.reduce()
    self.exprs.append(e)
    pass

  def post_load(self):
    # called after all input is read

    if len(self.exprs) == 1:
      self.sum = self.exprs[0]
      return
 
    cur = SN(None)
    cur.l = self.exprs[0]
    for e in self.exprs[1:]:
      if cur.r:
        outer = SN(None)
        outer.l = cur
        cur.parent = outer
        cur = outer
      cur.r = e

    self.sum = cur
    print(self.sum)

  def part1(self):
    print('===== Start part 1')
    self.reset()

    return self.sum.magnitude()


  def part2(self):
    print('===== Start part 2')
    self.reset()

    return 42


def check_reduce(s, expect, one_loop=False):
    e = SN.parse(s)
    e.reduce(one_loop=one_loop)
    got = str(e)
    if expect == got:
      print('PASS:', s, '=>', expect)
    else:
      print('FAIL:', s, '=>', got, 'expected', expect)
      sys.exit(1)
  

day18.sample_test("""[[1,2],[[3,4],5]]""", expect1=143, expect2=None)
day18.sample_test("""[[[[0,7],4],[[7,8],[6,0]]],[8,1]]""", expect1=1384)
day18.sample_test("""[[[[1,1],[2,2]],[3,3]],[4,4]]""", expect1=445)
day18.sample_test("""[[[[3,0],[5,3]],[4,4]],[5,5]]""", expect1=791)
day18.sample_test("""[[[[5,0],[7,4]],[5,5]],[6,6]]""", expect1=1137)
day18.sample_test("""[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]""", expect1=3488)
day18.sample_test("""
[1,1]
[2,2]
[3,3]
[4,4]
""", expect1=445)

check_reduce("[[[[[9,8],1],2],3],4]", expect="[[[[0,9],2],3],4]")
check_reduce("[7,[6,[5,[4,[3,2]]]]]", expect="[7,[6,[5,[7,0]]]]")
check_reduce("[[6,[5,[4,[3,2]]]],1]", expect="[[6,[5,[7,0]]],3]")
check_reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", expect="[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", one_loop=True)
check_reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", expect="[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
check_reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", expect="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

day18.sample_test("""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
""", expect1=445)

day18.sample_test("""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""", expect1=4140)


if __name__ == '__main__':
  day18.run_and_check('input.txt', expect1=None, expect2=None)
