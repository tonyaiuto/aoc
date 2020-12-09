"AOC 2020: day 8"

from collections import defaultdict

import intcode
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



class day8(object):

  def __init__(self):
    self.proc = intcode.Intcode()

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
      self.proc.mem.append(intcode.Ins(x[0], x[1]))

  def part1(self):
    self.proc.run(loop_detect=True)
    return self.proc.acc

  def part2(self):
    for i in range(len(self.proc.mem)):
      op = self.proc.mem[i]
      if op.opcode == 'nop':
        sub = intcode.Ins('jmp', op.arg)
      elif op.opcode == 'jmp':
        sub = intcode.Ins('nop', op.arg)
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
