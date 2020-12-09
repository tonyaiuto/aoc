

class Reader(object):

  def __init__(self, by_group=False, strip_lines=True, collect=False):
    self._nlines = 0
    self._ngroups = 0
    self._by_group = by_group
    self._strip_lines = strip_lines
    self._collect = collect
    self.all = []

  @property
  def nlines(self):
    return self._nlines

  @property
  def ngroups(self):
    return self._ngroups

  def _do_line(self, line):
    self._nlines += 1
    self._ngroups += 1
    if self._strip_lines:
      line = line.strip()
    if self._collect:
      self.all.append(line)
    return line

  def _do_group(self, group):
    pass


class StringReader(Reader):

  def __init__(self, inp, **kwargs):
    super(StringReader, self).__init__(**kwargs)
    self.inp = inp

  def next(self):
    if not self._by_group:
      for l in self.inp.split('\n'):
        yield self._do_line(l)
      return

    group = []
    for l in self.inp.split('\n'):
      self._nlines += 1
      if self._strip_lines:
        l = l.strip()
      if not l:
        if group:
          self._ngroups += 1
          if self._collect:
            self.all.append(group)
          yield group
          group = []
      else:
        group.append(l)

    if group:
      self._ngroups += 1
      if self._collect:
        self.all.append(group)
      yield group


class FileReader(Reader):

  def __init__(self, file, **kwargs):
    super(FileReader, self).__init__(**kwargs)
    self.file = file

  def next(self):
    with open(self.file, 'r') as inp:
      if not self._by_group:
        for line in inp:
          yield self._do_line(line)
        return

      group = []
      for line in inp:
        self._nlines += 1
        if self._strip_lines:
          line = line.strip()
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

  r = StringReader("""abc  \ndef\n\nghi""", strip_lines=False, collect=True)
  result = [l for l in r.next()]
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
