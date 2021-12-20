#!/usr/bin/env python3
"AOC 2021: day 18"

from collections import defaultdict
import copy
import sys

from tools import aoc

print("\n===")

VERBOSE = 1

LEFT = -1
RIGHT = -2
COMMA = -3

class SN(object):

  def __init__(self, n=0):
    self.n = n

  def __str__(self):
    o = {
        LEFT: '[',
        RIGHT: ']',
        COMMA: ',',
    }
    return ''.join([o[c] if c < 0 else str(c) for c in self.n])

  @staticmethod
  def parse(s):
    ret = SN()
    ret.raw = s
    ret.n = []
    for c in s:
      if c.isdigit():
        ret.n.append(int(c))
      else:
        ret.n.append({
            '[': LEFT,
            ']': RIGHT,
            ',': COMMA,
            }[c])
    return ret
 
  def magnitude(self):
    stack = []
    for v in self.n:
      if (len(stack) > 2 and v == RIGHT
          and stack[-1] >= 0
          and stack[-2] == COMMA
          and stack[-3] >= 0):
        mag = 3 * stack[-3] + 2 * stack[-1]
        stack.pop()
        stack.pop()
        stack.pop()
        stack[-1] = mag
        # print(" mag", v, '=>', mag, stack)
      else :
        stack.append(v)
    return stack[0]

  def reduce(self, one_loop=False):

    # print("\nREDUCE:", self.n)
    while True:
      if not self.check_explode():
        if not self.check_split():
          return
      if one_loop:
        return

    print('should not reach here ==================')
    return

  def check_explode(self):
    n_deep = 0
    for i, v in enumerate(self.n):
      # print(v)
      if v == LEFT:
        n_deep += 1
      elif v == RIGHT:
        n_deep -= 1
      elif n_deep > 4:
        # print("Explode me at", self.n[i:])
        # print('  ALL', self.n)
        for left_i in range(i-1, -1, -1):
          if self.n[left_i] >= 0:
            self.n[left_i] += self.n[i]
            break
        left = self.n[0:(i-1)]
        # print(' LEFT', left)
        for right_i in range(i+3, len(self.n)):
          if self.n[right_i] >= 0:
            self.n[right_i] += self.n[i+2]
            break
        right = self.n[i+4:]
        # print('RIGHT', right)
        final = left + [0] + right
        self.n = final
        # print('FINAL', final, str(self))
        return True
    return False

  def check_split(self):
    for i, v in enumerate(self.n):
      if v >= 10:
        rep = [LEFT, v // 2, COMMA, v - (v // 2), RIGHT]
        # print('SPLIT AT', i, v, rep)
        self.n = self.n[0:i] + rep + self.n[i+1:]
        # print('       >', str(self))
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

  def post_load(self):
    # called after all input is read
    return
 
  def part1(self):
    print('===== Start part 1')
    self.reset()

    root = combine(self.exprs, verbose=self.trace_sample)
    self.sum = root
    if self.trace_sample:
      print('Final:', self.sum)
    return self.sum.magnitude()

  def part2(self):
    print('===== Start part 2')
    self.reset()

    ret = 0
    for i in range(len(self.exprs)):
      for j in range(i+1, len(self.exprs)):

        exprs = [
            copy.deepcopy(self.exprs[i]),
            copy.deepcopy(self.exprs[j]),
        ]
        root = combine(exprs, verbose=self.trace_sample)
        mag = root.magnitude()
        ret = max(ret, mag)
        # print('%-20.20s + %-20.20s => %d' % (str(e1), str(e2), mag))

        #if str(e2).startswith('[[2,[[7,7'):
        #  print('%-20.20s + %-20.20s => =============' % (str(e2), str(e1)))

        exprs = [
            copy.deepcopy(self.exprs[j]),
            copy.deepcopy(self.exprs[i]),
        ]
        root = combine(exprs, verbose=self.trace_sample)
        mag = root.magnitude()
        ret = max(ret, mag)
        # print('%-20.20s + %-20.20s => %d' % (str(e2), str(e1), mag))

    return ret

def combine(exprs, verbose=False):
  if len(exprs) == 1:
    return exprs[0]
  comb = SN()
  comb.n = [LEFT] + exprs[0].n + [COMMA] + exprs[1].n + [RIGHT]
  comb.reduce()
  for e in exprs[2:]:
    comb.n = [LEFT] + comb.n + [COMMA] + e.n + [RIGHT]
    comb.reduce()
  return comb


def check_reduce(s, expect, one_loop=False):
  s = s.strip()
  e = SN.parse(s)
  e.reduce(one_loop=one_loop)
  got = str(e)
  if expect == got:
    print('PASS:', s, '=>', expect)
  else:
    print('FAIL:', s, '=>', got, 'expected', expect)
    sys.exit(1)

def check_combine(s, expect, one_loop=False):
  s = s.strip()
  exprs = []
  for line in s.split('\n'):
    if line:
      e = SN.parse(line.strip())
      e.reduce()
      exprs.append(e)

  root = combine(exprs)
  got = str(root)
  if expect == got:
    print('PASS:', s, '=>', expect)
  else:
    print('FAIL:', s, '    got', got, '\nexpected', expect)
    sys.exit(1)
  

check_reduce("[[[[[9,8],1],2],3],4]", expect="[[[[0,9],2],3],4]")
check_reduce("[7,[6,[5,[4,[3,2]]]]]", expect="[7,[6,[5,[7,0]]]]")
check_reduce("[[6,[5,[4,[3,2]]]],1]", expect="[[6,[5,[7,0]]],3]")
check_reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", expect="[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", one_loop=True)
check_reduce("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", expect="[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
check_reduce("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", expect="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

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

check_combine("""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
""", expect="[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")

check_combine("""
[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
""", expect="[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")

check_combine("""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
""", expect="[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")

check_combine("""
[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
""", expect="[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]")

check_combine("""
[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
[7,[5,[[3,8],[1,4]]]]
""", expect="[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]")

check_combine("""
[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
[[2,[2,2]],[8,[8,1]]]
""", expect="[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]")

check_combine("""
[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
[2,9]
""", expect="[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]")

check_combine("""
[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
[2,9]
""", expect="[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]")

check_combine("""
[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
[1,[[[9,3],9],[[9,0],[0,7]]]]
""", expect="[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]")

check_combine("""
[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
[[[5,[7,4]],7],1]
""", expect="[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]")

check_combine("""
[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
[[[[4,2],2],6],[8,7]]
""", expect="[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")


day18.sample_test("""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
""", expect1=3488)


day18.sample_test("""
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
""", expect1=3993)

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
""", expect1=4140, expect2=3993)


VERBOSE = False

if __name__ == '__main__':
  day18.run_and_check('input.txt', expect1=4088, expect2=4536)
  pass
