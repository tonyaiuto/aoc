

class Reader(object):

  def __init__(self, by_group=False, strip_lines=True):
    self._nlines = 0
    self._ngroups = 0
    self._by_group = by_group
    self._strip_lines = strip_lines
    self.all = []

  @property
  def nlines(self):
    return self._nlines

  @property
  def ngroups(self):
    return self._ngroups

  def _do_line(self, line):
    self._nlines += 1
    if self._strip_lines:
      line = line.strip()
    return line

  def _do_group(self, group):
    pass


class StringReader(Reader):

  def __init__(self, inp, **kwargs):
    super(StringReader, self).__init__(**kwargs)
    self.inp = inp

  def next(self):
    if not self._by_group:
      for line in self.inp.split('\n'):
        self._ngroups += 1
        yield self._do_line(line)
      return

    group = []
    for line in self.inp.split('\n'):
      line = self._do_line(line)
      # TODO: other delimiter formats?
      if not line:
        if group:
          self._ngroups += 1
          yield group
          group = []
      else:
        group.append(line)

    if group:
      self._ngroups += 1
      yield group

  def load(self):
    for v in self.next():
      self.all.append(v)
    return self.all


class FileReader(StringReader):

  def __init__(self, file, **kwargs):
    self.file = file
    with open(file, 'r') as inp:
      s = inp.read()
    super(FileReader, self).__init__(s, **kwargs)


def tests():
  r = StringReader("""abc  \ndef\n\nghi""")
  result = [l for l in r.next()]
  assert result == ['abc', 'def', '', 'ghi']
  r = StringReader("""abc  \ndef\n\nghi""", strip_lines=False)
  result = [l for l in r.next()]
  assert result == ['abc  ', 'def', '', 'ghi']

  r = StringReader("""
group 1

group 2
group 2

group 3
group 3
group 3

""", by_group=True)
  result = [l for l in r.next()]
  # print(result)
  assert result == [['group 1'], ['group 2', 'group 2'], ['group 3', 'group 3', 'group 3']]



if __name__ == '__main__':
  tests()



def tests():
  r = StringReader("""abc  \ndef\n\nghi""")
  result = [l for l in r.next()]
  assert result == ['abc', 'def', '', 'ghi']

  r = StringReader("""abc  \ndef\n\nghi""", strip_lines=False)
  result = [l for l in r.next()]
  assert result == ['abc  ', 'def', '', 'ghi']

  r = StringReader("""abc  \ndef\n\nghi""", strip_lines=False)
  result = r.load()
  assert result == ['abc  ', 'def', '', 'ghi']
  assert r.all == ['abc  ', 'def', '', 'ghi']

  r = StringReader("""
group 1

group 2
group 2

group 3
group 3
group 3

""", by_group=True)
  result = [l for l in r.next()]
  # print(result)
  assert result == [['group 1'], ['group 2', 'group 2'], ['group 3', 'group 3', 'group 3']]

  r = FileReader('groups.txt', by_group=True)
  result = [l for l in r.next()]
  # print(result)
  assert result == [['group 1'], ['group 2', 'group 2'], ['group 3', 'group 3', 'group 3']]



if __name__ == '__main__':
  tests()
