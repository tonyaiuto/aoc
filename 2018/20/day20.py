"""aoc 2018 day 20"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import Queue
import sys

_VERBOSE = 0
_PART2 = False



class Regex(object):

  def __init__(this, fixed=None, exprs=None, branches=None):
    this.fixed_path = fixed
    this.exprs = exprs or []
    this.branches = branches or []
    this.nil = not (fixed or exprs or branches)
    # if this.nil:
    #   print('======= null expr')

  @staticmethod
  def FromString(s):
    inp_stream = iter(s)
    c = inp_stream.next()
    if c != '^':
      raise ValueError('Regex must start with ^: %s' % s)
    c = inp_stream.next()
    try:
      ret, c = Regex._ParseExpr(c, inp_stream)
    except Exception as e:
      rest = ''
      try:
        for i in range(50):
          rest += inp_stream.next()
      except:
        pass
      e.Print(sys.stdout)
      print('Fail to parse at: %s' % rest)
      raise e

    if c != '$':
      raise ValueError('Regex must end with $: %s' % s)
    return ret

  @staticmethod
  def _ParseExpr(c, inp_stream):
    expressions = []
    ret = None
    got_term = True
    while got_term:
      got_term = False
      v, c  = Regex._ParseFixed(c, inp_stream)
      if v:
        expressions.append(v)
        got_term = True
      v, c  = Regex._ParseBranch(c, inp_stream)
      if v:
        got_term = True
        expressions.append(v)
    if expressions:
      ret = Regex(exprs=expressions)
    return ret, c

  @staticmethod
  def _ParseFixed(c, inp_stream):
    dirs = ''
    ret = None
    while c in 'NSEW':
      dirs += c
      c = inp_stream.next()
    if dirs:
      ret = Regex(fixed=dirs)
      # print('got fixed: %s' % ret)
    return ret, c

  @staticmethod
  def _ParseBranch(c, inp_stream):
    if c != '(':
      return None, c
    c = inp_stream.next()
    branches = []
    while True:
      if c == ')':
        # print('got terminating )')
        c = inp_stream.next()
        return Regex(branches=branches), c

      v, c  = Regex._ParseExpr(c, inp_stream)
      if v:
        # print('got expr: %s' % v)
        branches.append(v)
      elif c == '|':
        # print('got |')
        c = inp_stream.next()
        if c == ')':
          branches.append(Regex())
      else:
        break
    print('expected more in parse branch')
    return None, c

  def __str__(this):
    if this.fixed_path:
      return this.fixed_path
    if this.branches:
      ret = '('
      ret += '|'.join([str(b) for b in this.branches])
      ret += ')'
      return ret
    if this.exprs:
      return  ''.join([str(b) for b in this.exprs])

  def Print(this, out):
    if this.fixed_path:
      out.write(this.fixed_path)
    for e in this.exprs:
      e.Print(out)
    if this.branches:
      out.write('(')
      for b_i in range(len(this.branches)):
        this.branches[b_i].Print(out)
        if b_i < len(this.branches) - 1:
          out.write('|')
      out.write(')')


def ShortestPath(r):
  if r.fixed_path:
    # print('%s => %d' % (r.fixed_path, len(r.fixed_path)))
    return len(r.fixed_path)
  if r.exprs:
    ret = 0
    for e in r.exprs:
      ret += ShortestPath(e)
    return ret
  if r.branches:
    best = 0
    for b in r.branches:
      if b.nil:
        return 0
      b_len = ShortestPath(b)
      if b_len > best:
        best = b_len
    return best
  return 0


def part1(regex):
  print('Furthest room requires passing %d doors' % ShortestPath(regex))



visited = set()

def P2(r, path_so_far, x, y):
  global visited

  if r.fixed_path:
    n_rooms = 0
    for dir in r.fixed_path:
       path_so_far += 1
       if dir == 'E':
         x += 1
       elif dir == 'W':
         x -= 1
       elif dir == 'N':
         y -= 1
       elif dir == 'S':
         y += 1
       if (x, y) not in visited:
         visited.add((x,y))
         if path_so_far >= 1000:
           n_rooms += 1
    print('path_so_far=%d at %s' % (path_so_far, r.fixed_path))
    return path_so_far, n_rooms, x, y
  if r.exprs:
    n_rooms = 0
    e_i = 0
    for e in r.exprs:
      e_i += 1
      print(' e[%d], path_so_far=%d' % (e_i, path_so_far))
      path_so_far, n_r, x, y = P2(e, path_so_far, x, y)
      n_rooms += n_r
    return path_so_far, n_rooms, x, y
  if r.branches:
    best = 0
    n_rooms = 0
    b_i = 0
    save_x = x
    save_y = y
    for b in r.branches:
      b_i += 1
      p_len, n_r, x, y = P2(b, path_so_far, save_x, save_y)
      print('  branch %d, path_so_far=%d' % (b_i, path_so_far))
      n_rooms += n_r   
      if p_len > best:
        best = p_len
        best_x = x
        best_y = y
      if b.nil:
        return path_so_far, n_rooms, save_x, save_y
    print('  branches done, path_so_far=%d, %d rooms' % (path_so_far, n_rooms))
    return best, n_rooms, best_x, best_y
  print('Nil, path=%d' % path_so_far)
  return path_so_far, 0, x, y


def part2(regex):
  visited.add((0, 0))
  path_len, n_rooms, x, y = P2(regex, 0, 0, 0) 
  print('%d rooms, max path=%d' % (n_rooms, path_len))
  print('%d visited rooms' % len(visited))


if __name__ == '__main__':
  dump = False
  iarg = 1
  expr = None
  while iarg < len(sys.argv) and sys.argv[iarg][0] == '-':
    if sys.argv[iarg] == '-v':
      _VERBOSE += 1
      iarg += 1
    if sys.argv[iarg] == '-d':
      dump = True
      iarg += 1
    if sys.argv[iarg] == '-2':
      _PART2 = True
      iarg += 1
    if sys.argv[iarg] == '-e':
      expr = sys.argv[iarg+1]
      iarg += 2

  if expr:
    regex = Regex.FromString(expr)
  else:
    with open(sys.argv[iarg]) as inp:
      regex = Regex.FromString(inp.read())
  if dump:
    sys.stdout.write('^')
    regex.Print(sys.stdout)
    print('$')

  part1(regex)
  part2(regex)
