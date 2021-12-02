"""aoc core."""

from tools import reader


class aoc(object):

  def __init__(self, reader_params={}):
    self.result1 = None
    self.result2 = None
    self.trace = True
    self.all_input = None
    self.reader_params = {
        'by_group': False,
        'skip_first_blank': True,
        'strip_lines': True,
        'verbose': False,
    }
    self.reader_params.update(reader_params)

  def reset(self):
    pass

  def load_file(self, file):
    self.all_input = reader.FileReader(file, **self.reader_params).load()
    for x in self.all_input:
      self.do_line(x)
    self.post_load()

  def load_str(self, s):
    self.all_input = reader.StringReader(s, **self.reader_params).load()
    for x in self.all_input:
      self.do_line(x)
    self.post_load()

  def do_line(self, line):
    pass

  def post_load(self):
    pass

  def part1(self):
    print('You must implement part1()')

  def part2(self):
    print('You must implement part1()')

  @classmethod
  def run_and_check(cls, input, expect1=None, expect2=None, tag=None):
    solver = cls()
    solver.load_file(input)
    tag = tag or type(solver).__name__
    res = solver.part1()
    solver.result1 = res
    print('part1', res)
    if expect1 and  expect1 != res:
      print('FAIL: %s.part1:' % tag, 'expect', expect1, 'got', res)
      assert expect1 == res

    solver = cls()
    solver.load_file(input)
    res = solver.part2()
    solver.result2 = res
    print('part2', res)
    if expect2 and  expect2 != res:
      print('FAIL: %s.part2:' % tag, 'expect', expect2, 'got', res)
      assert expect2 == res

  @classmethod
  def sample_test(cls, s, expect1=None, expect2=None, tag=None):
    solver = cls()
    tag = tag or 'sample'
    solver.load_str(s)
    res = solver.part1()
    if expect1 != res:
      print('FAIL: %s.part1:' % tag, 'expect', expect1, 'got', res)
      assert expect1 == res

    if expect2:
      solver = cls()
      solver.load_str(s)
      res = solver.part2()
      if expect2 != res:
        print('FAIL: %s.part2:' % tag, 'expect', expect2, 'got', res)
        assert expect2 == res
    print('PASS: %s' % (tag or cls.__class__.__name__))
