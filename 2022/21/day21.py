#!/usr/bin/env python3
"AOC 2021: day 21"

from collections import defaultdict
import copy
import heapq
import itertools
import math

from tools import aoc
from tools import gridutils


class Monkey(object):

  monkeys = {}

  def __init__(self, from_string):
    p = from_string.strip().split(':')
    self.id = p[0]
    Monkey.monkeys[self.id] = self
    rest = p[1].strip()
    if rest[0].isdigit():
      self.n = int(rest)
      self.is_constant = True
      return
    self.is_constant = False
    self.n = -1
    self.a_s = rest[0:4]
    self.op = rest[5]
    self.b_s = rest[7:]

  def __str__(self):
    ret = self.id + ': '
    if self.n >= 0:
      ret += str(self.n)
    else:
      ret += self.a_s + '.%c.' % self.op + self.b_s
    return ret


class day21(aoc.aoc):

  def __init__(self):
    super(day21, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.monkeys = []

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    # called for each line of input
    m = Monkey(from_string=line)
    # print(m)
    self.monkeys.append(m)

  def post_load(self):
    # called after all input is read
    for m in self.monkeys:
      if m.n >= 0:
        continue
      m.a = Monkey.monkeys[m.a_s]
      m.b = Monkey.monkeys[m.b_s]


  def part1(self):
    print('===== Start part 1')
    self.reset()

    root = Monkey.monkeys['root']
    ret = self.eval(root)
    return ret

  def eval(self, monkey):
    if monkey.n >= 0:
      return monkey.n
    a = self.eval(monkey.a)
    b = self.eval(monkey.b)
    if monkey.op == '+':
      return a + b
    if monkey.op == '-':
      return a - b
    if monkey.op == '*':
      return a * b
    if monkey.op == '/':
      return a // b


  def part2(self):
    print('===== Start part 2')
    self.reset()

    root = Monkey.monkeys['root']
    human = Monkey.monkeys['humn']
    human.is_constant = False

    in_left = find_monkey(root.a, human)
    in_right = find_monkey(root.b, human)
    print('monkey left', in_left, 'right', in_right)
    if in_left:
      x = root.b
      root.b = root.a
      root.a = x

    print('left', print_expr(root.a))
    print('right', print_expr(root.b))
    simplify(root.a)
    print('simple left', print_expr(root.a))
    simplify(root.b)
    print('simple right', print_expr(root.b))

    assert root.a.is_constant
    e = root.b
    val = root.a.n
    for i in range(len(self.monkeys)):
      n_e, n_val = reduce(e, val)
      if not n_e:
        print("HIT THE DECK")
        break
      print('  reduce', n_val, '==', print_expr(n_e))
      if n_e == human:
        return n_val
      e = n_e
      val = n_val

    """
    # Good enought for sample
    for h in range(1000):
       human.n = h
       left = self.eval(root.a)
       right = self.eval(root.b)
       if left == right:
         return h
       # print(h, left, right)
    """
  
def simplify(m):
  if m.id == 'humn':
    return
  if m.is_constant:
    return
  simplify(m.a)
  simplify(m.b)
  if m.a.is_constant and m.b.is_constant:
    if m.op == '+':
      m.n = m.a.n + m.b.n
    if m.op == '-':
      m.n = m.a.n - m.b.n
    if m.op == '*':
      m.n = m.a.n * m.b.n
    if m.op == '/':
      m.n =  m.a.n // m.b.n
    m.is_constant = True

def reduce(m, val):
  # reduce e op constant == val  =>  e = val'
  if m.is_constant:
    return None, val
  if m.a.is_constant:
    if m.op == '/':  #  K / X = V   =>  X == K / V
      return m.b, m.a.n // val
    if m.op == '*':  #  K * X = V   =>  X == V / K
      return m.b, val // m.a.n
    if m.op == '+':  #  K + X = V   =>  X == V - K
      return m.b, val - m.a.n
    if m.op == '-':  #  K - X = V   =>  X == K - V
      return m.b, m.a.n - val
  elif m.b.is_constant:
    if m.op == '/':  #  X / K = V   =>  X == V * K
      return m.a, val * m.b.n
    if m.op == '*':  #  X * K = V   =>  X == V / K
      return m.a, val // m.b.n
    if m.op == '+':  #  X + K = V   =>  X == V - K
      return m.a, val - m.b.n
    if m.op == '-':  #  X - K = V   =>  X == V + K
      return m.a, val + m.b.n
  return None, val


def print_expr(m):
  if m.id == 'humn':
    return 'HUMAN'
  if m.n > 0:
    return str(m.n)
  return ''.join([
      '(',
      print_expr(m.a),
      m.op,
      print_expr(m.b),
      ')',])

def find_monkey(tree, m):
  if tree.n >= 0:
    return False
  if tree.a == m or tree.b == m:
    return True
  return find_monkey(tree.a, m) or find_monkey(tree.b, m)


day21.sample_test("""
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""", expect1=152, expect2=301)


if __name__ == '__main__':
  day21.run_and_check('input.txt', expect1=41857219607906, expect2=None)
