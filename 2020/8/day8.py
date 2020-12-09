"AOC 2020: day 8"

from collections import defaultdict

from tools import reader


def sample_test(s, expect):
  puzz = day8()
  puzz.load_str(s)
  print(puzz.proc.mem)
  res = puzz.part1()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res

def sample_test2(s, expect):
  puzz = day8()
  puzz.load_str(s)
  print(puzz.proc.mem)
  res = puzz.part2()
  if expect != res:
    print('FAIL: expect', expect, 'got', res)
    assert expect == res


def main(input):
  puzz = day8()
  puzz.load_file(input)
  res = puzz.part1()
  assert res == 1832
  print('part1', res)
  res = puzz.part2()
  print('part2', res)


class Ins(object):

  def __init__(self, opcode, arg):
    self.opcode = opcode
    self.arg = int(arg)

  def __repr__(self):
    return '%s %d' % (self.opcode, self.arg)


class Proc(object):

  def __init__(self, trace=False):
    self.mem = []
    self.pc = 0
    self.acc = 0
    self.trace = trace

  def run(self, loop_detect=False):
    self.pc = 0
    self.acc = 0
    n_cycles = 0
    seen = set()
    while self.pc != len(self.mem):
      n_cycles += 1
      if n_cycles > 1000:
        # print('====== infinite loop')
        return 'loop'
      if loop_detect:
        if self.pc in seen:
          print('DONE', self.acc)
          return
        seen.add(self.pc)
      op = self.mem[self.pc]
      if self.trace:
        print('pc', self.pc, 'acc', self.acc, op)
      self.do_op(op)
    return


  def do_op(self, op):
    if op.opcode == 'nop':
      self.pc += 1
      return
    if op.opcode == 'acc':
      self.acc += op.arg
      self.pc += 1
      return
    if op.opcode == 'jmp':
      self.pc += op.arg
      return
    print('bad opcode', op)



class day8(object):

  def __init__(self):
    self.proc = Proc()

  def load_file(self, file):
    all = reader.FileReader(file).load()
    for x in all:
      self.do_line(x)

  def load_str(self, s):
    all = reader.StringReader(s).load()
    for x in all:
      self.do_line(x)

  def do_line(self, line):
    if line:
      x = line.split(' ')
      self.proc.mem.append(Ins(x[0], x[1]))

  def part1(self):
    self.proc.run(loop_detect=True)
    return self.proc.acc

  def part2(self):
    for i in range(len(self.proc.mem)):
      op = self.proc.mem[i]
      if op.opcode == 'nop':
        sub = Ins('jmp', op.arg)
      elif op.opcode == 'jmp':
        sub = Ins('nop', op.arg)
      else:
         continue
      self.proc.mem[i] = sub
      err = self.proc.run()
      if not err:
        return self.proc.acc
      self.proc.mem[i] = op

    print('========= fail')
    return None


sample_test("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""", 5)

sample_test2("""nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""", 8)


if __name__ == '__main__':
  main('input.txt')
