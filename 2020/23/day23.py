"AOC 2020: day 23"

from tools import reader

def sample_test(s, expect, expect2=None):
  puzz = day23()
  puzz.load_str(s)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

  if expect2:
    puzz = day23()
    puzz.load_str(s)
    res = puzz.part2()
    if expect2 != res:
      print('FAIL: expect', expect2, 'got', res)
      assert expect2 == res


def main(input, e1=None, e2=None):
  puzz = day23()
  puzz.load_file(input)
  res = puzz.part1()
  print('part1', res)
  if e1 and  e1 != res:
    print('FAIL: expect', e1, 'got', res)
    assert e1 == res

  puzz = day23()
  puzz.load_file(input)
  res = puzz.part2()
  print('part2', res)
  if e2 and  e2 != res:
    print('FAIL: expect', e2, 'got', res)
    assert e2 == res


class Cup(object):

  cups = {}

  def __init__(self, n):
    self.n = n
    self.nxt = None
    Cup.cups[n] = self

  def __str__(self):
    return 'cup %d -> %d -> %d ...' % (self.n, self.nxt.n, self.nxt.nxt.n)

  def printlist(self):
    ret = [str(self.n)]
    cur = self.nxt
    while cur != self:
      ret.append(str(cur.n))
      cur = cur.nxt
    print(' '.join(ret))


class day23(object):

  def __init__(self):
    self.result1 = None
    self.result2 = None
    self.trace = True

  def reset(self):
    pass

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)
    self.post_load(all)

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)
    self.post_load(all)

  def do_line(self, line):
    pass

  def post_load(self, all):
    cups = [int(c) for c in str(all[0])]
    self.clist = cups
    self.cur = Cup(cups[0])
    last = self.cur
    self.l = 0
    for c in cups[1:]:
      nxt = Cup(c)
      last.nxt = nxt
      last = nxt
      self.l = max(self.l, c)
    self.last_cup = last
    nxt.nxt = self.cur

    print('cur:', self.cur)
    print('last:', self.last_cup)

  def move(self):
    pick = self.cur.nxt
    picki = [pick.n, pick.nxt.n, pick.nxt.nxt.n]
    after_pick = pick.nxt.nxt.nxt
    self.cur.nxt = after_pick
    dst = self.cur.n - 1
    if dst == 0:
      dst = self.l
    self.cur = after_pick
    while dst in picki:
      dst = dst - 1
      if dst == 0:
        dst = self.l
    dst_node = Cup.cups[dst]
    pick.nxt.nxt.nxt = dst_node.nxt
    dst_node.nxt = pick

  def part1(self):
    print('===== Start part 1')
    self.reset()
    self.cur.printlist()

    for i in range(100):
      self.move()
      if i < 5 or i > 98:
        self.cur.printlist()

    c = Cup.cups[1].nxt
    res = ''
    for i in range(self.l-1):
      res += str(c.n)
      c = c.nxt
    self.result1 = int(res)

    print('part1', self.result1)
    return self.result1

  def part2list(self):
    print('===== Start part 2')
    self.reset()

    last_cup = Cup.cups[self.last_cup.n]
    self.l = 1000000
    for i in range(9, 1000000):
      last_cup.nxt = Cup(i+1)
      last_cup = last_cup.nxt
    last_cup.nxt = self.cur
    print(self.cur)
    print(last_cup)

    for i in range(10000000):
      if i % 100000 == 0:
        print('move %6d' % i, str(self.cur))
      self.move()

    cup1 = Cup.cups[1]
    print(cup1)
    self.result2 = cup1.nxt.n * cup1.nxt.nxt.n
    print('part2', self.result2)
    return self.result2

  def part2(self):
    print('===== Start part 2 - fast way')

    # Alt
    old_last = self.l
    self.l = 1000000
    nxt = [0] * (self.l + 1)

    cur = self.clist[0]
    at = cur
    for c in self.clist[1:]:
      nxt[at] = c
      at = c
    nxt[at] = 10
    print(len(nxt))
    for i in range(10, self.l):
      nxt[i] = i+1
    nxt[self.l] = self.clist[0]
    print('start', nxt[0:12])
    print('last', nxt[-3:])

    for i in range(10000000):
      if i < 5 or (i % 100000 == 0):
        print('move %6d' % i, nxt[cur:cur+10])
      pick = nxt[cur]
      p2 = nxt[pick]
      p3 = nxt[p2]
      picki = [pick, p2, p3]
      after_pick = nxt[p3]

      nxt[cur] = after_pick
      dst = cur - 1
      if dst == 0:
        dst = self.l
      cur = after_pick
      while dst in picki:
        dst = dst - 1
        if dst == 0:
          dst = self.l
      nxt[p3] = nxt[dst]
      nxt[dst] = pick

    cup1 = nxt[1]
    print('nxt[1]', cup1)
    self.result2 = cup1 * nxt[cup1]
    print('part2', self.result2)
    return self.result2


sample_test("""389125467""", 67384529, 149245887792)


if __name__ == '__main__':
  # 198753462
  main('input.txt', 62934785, 693659135400)
