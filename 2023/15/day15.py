#!/usr/bin/env python3
"AOC 2023: day 15"

from tools import aoc


class Step(object):

  def __init__(self, s):
    self.s = s
    t = s.split('=')
    if len(t) > 1:
      self.label = t[0]
      self.focal = int(t[1])
    else:
      self.label = s
      self.focal = 0
    self.dash = s.endswith('-')
    assert self.dash == (s.find('-') > 0)
    if self.dash:
      self.label = s[0:-1]
    # print(self.s, 'focal', self.focal, 'dash', self.dash, self.label)

  def __str__(self):
    return str(self)

  def __repr__(self):
    return '%s %d' % (self.label, self.focal)

  def hash(self):
    return self.hash_str(self.s)

  def hash_label(self):
    return self.hash_str(self.label)

  @staticmethod
  def hash_str(s):
    ret = 0
    for c in s:
      ret = (ret + ord(c)) * 17 % 256
    # print('hash(%s)=%d' % (self.s, ret))
    return ret

class day15(aoc.aoc):

  def __init__(self):
    super(day15, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.steps = []
    self.part1_answer = 0
    self.box = []
    for i in range(256):
      self.box.append([])

  def do_line(self, line):
    # called for each line of input
    # rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
    for s in line.split(','):
      step = Step(s)
      self.part1_answer += step.hash()
      self.steps.append(step)

  def part1(self):
    print('===== Start part 1')
    print('part1', self.part1_answer)
    return self.part1_answer

  def part2(self):
    print('===== Start part 2')
    for step in self.steps:
      box_i = step.hash_label()
      if step.focal > 0:
        add_or_replace(self.box[box_i], step)
      else:
        assert step.dash
        self.box[box_i] = remove(self.box[box_i], step.label)
      if self.doing_sample:
        print('--', step.s)
        self.print_boxes()

    ret = 0
    for i in range(256):
      for il, lens in enumerate(self.box[i]):
        focus_power = (i + 1) * (il + 1) * lens.focal
        ret += focus_power
    print('part2', ret)
    return ret

  def print_boxes(self):
    for i in range(256):
      if self.box[i]:
        print('%3d' % i, self.box[i])


def add_or_replace(box, new_lens):
  for ic, lens in enumerate(box):
    if lens.label == new_lens.label:
      box[ic] = new_lens
      return
  box.append(new_lens)


def remove(box, label):
  return [lens for lens in box if lens.label != label]


assert Step("HASH").hash() == 52
assert Step('rn=1').hash() == 30
assert Step('cm-').hash() == 253
assert Step('qp=3').hash() == 97
assert Step('cm=2').hash() == 47
assert Step('qp-').hash() == 14
assert Step('pc=4').hash() == 180
assert Step('ot=9').hash() == 9
assert Step('ab=5').hash() == 197
assert Step('pc-').hash() == 48
assert Step('pc=6').hash() == 214
assert Step('ot=7').hash() == 231

day15.sample_test("""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
""", expect1=1320, expect2=145)


if __name__ == '__main__':
  day15.run_and_check('input.txt', expect1=519041, expect2=260530)
