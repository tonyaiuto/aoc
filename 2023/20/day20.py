#!/usr/bin/env python3
"AOC 2023: day 20"

from collections import defaultdict
from collections import deque

from tools import aoc
from tools import gridutils
from tools import qparser

FF = 1
CONJ = 2
CAST = 3

HIGH = True
LOW = False

class Module(object):
 
  # &pf -> pp, tv, rl, pm, hk
  def __init__(self, s):
    parts = s.replace(', ', ' ').replace('  ', ' ').split(' ')
    assert parts[1] == '->'
    name = parts[0]
    if name[0] == '%':
      self.name = name[1:]
      self.type = FF
    elif name[0] == '&':
      self.name = name[1:]
      self.type = CONJ
      self.inputs = {}
    elif name == 'broadcaster':
      self.name = name
      self.type = CAST
    else:
      print("WACKY", s)
      assert False
    self.outputs_s = parts[2:]
    if not self.outputs_s:
      self.outputs = []
    self.state = False

  def __str__(self):
    return '%s %d -> %s' % (self.name, self.type, self.outputs_s)

  def __repr__(self):
    return self.name


class day20(aoc.aoc):

  def __init__(self):
    super(day20, self).__init__(
        reader_params={
            'by_group': False,
            'skip_first_blank': True,
            'strip_lines': True,
            'verbose': False,
        })
    self.trace = True
    self.modules = {}

  def reset(self):
    # for future use
    pass

  def do_line(self, line):
    m = Module(line)
    self.modules[m.name] = m
    # print(m)

  def post_load(self):
    # called after all input is read
    # do the lookups and find the conjunctions
    to_add = {}
    for m in self.modules.values():
      m.outputs = []
      for out in m.outputs_s:
        actual = self.modules.get(out)
        if not actual:
          actual = to_add.get(out)
        if not actual:
          print("Creating dummy sink", out)
          actual = Module("%%%s ->" % out)
          to_add[actual.name] = actual
        m.outputs.append(actual)

      for out in m.outputs:
        if out.type == CONJ:
          out.inputs[m] = LOW

    for m in to_add.values():
      self.modules[m.name] = m
    self.broadcaster = self.modules['broadcaster']
    pass


  def part1(self):
    print('===== Start part 1')
    self.reset()

    if self.doing_sample:
      for m in self.modules.values():
        if m.type == CONJ:
          print('CONJ', m, "===", m.inputs)

    self.counts = {'low': 0, 'high': 0}
    for i in range(1000):
      self.do_button()
    ret = self.counts['low'] * self.counts['high']
    print(self.counts, '=>', ret)
    return ret


  def do_button(self):
    pulses = deque()
    self.send_pulse(None, self.broadcaster, LOW, pulses)
    while len(pulses) > 0:
      # print(pulses)
      what = pulses.popleft()
      from_m = what[0]
      to_m = what[1]
      pulse = what[2]
      self.send_pulse(from_m, to_m, pulse, pulses)

  def send_pulse(self, from_m, to_module, pulse, pulses):
    self.counts['high' if pulse else 'low'] += 1
    if to_module.type == CAST:
      for m in to_module.outputs:
        pulses.append((to_module, m, pulse))
      return

    if to_module.type == FF:
      if pulse == HIGH:
        return
      to_module.state = not to_module.state
      for m in to_module.outputs:
        pulses.append((to_module, m, to_module.state))
      return

    if to_module.type == CONJ:
      to_module.inputs[from_m] = pulse
      all_high = True
      for state in to_module.inputs.values():
        if state != HIGH:
          all_high = False
          break
      if all_high:
        pulse = LOW
      else:
        pulse = HIGH
      for m in to_module.outputs:
        pulses.append((to_module, m, pulse))
      return

    assert "can not reach" == 'here'


  def part2(self):
    print('===== Start part 2')
    self.reset()


    return 42


day20.sample_test("""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""", expect1=32000000, expect2=None)

day20.sample_test("""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""", expect1=11687500, expect2=None)


if __name__ == '__main__':
  day20.run_and_check('input.txt', expect1=711650489, expect2=None)
