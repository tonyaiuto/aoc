"""Quick Parser.

YMMV

Example:
	qp.Parser([
	  qp.Text('name', allow_space=True),
	  qp.Literal(':'),
	  qp.Number('r1_low'),
	  qp.Literal('-'),
	  qp.Number('r1_high'),
	  qp.Literal('or'),
	  qp.Number('r2_low'),
	  qp.Literal('-'),
	  qp.Number('r2_high'),
        ])

arrival platform: 40-550 or 570-956
arrival track: 49-854 or 863-953
class: 48-601 or 614-964
duration: 27-698 or 715-962
price: 38-781 or 800-970
route: 47-824 or 842-965
row: 45-219 or 241-955
seat: 47-388 or 401-954
train: 42-906 or 919-965
type: 40-726 or 733-955
"""

"""
class Result(dict):
  def __init__(self):
    pass

  def __setattr__(self, name, value):
    pass

  def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)
"""


class _Dummy(object):

  def __init__(self):
    pass


class Error(Exception):

  def __init__(self, message, text):
    self.message = message
    self.text = text
  


class FBase(object):

  def __init__(self, name, eat_leading_ws=True):
    self.name = name
    self.eat_leading_ws = eat_leading_ws


  def assign(self, obj, value):
    obj.__dict__[self.name] = value


def check_assignable():
  a = FBase('foo')
  b = FBase('answer')

  o = _Dummy()
  a.assign(o, 'bar')
  b.assign(o, 42)
  assert o.foo == 'bar'
  assert o.answer == 42


class Literal(FBase):

  def __init__(self, text, eat_leading_ws=True):
    super(Literal, self).__init__(name=text, eat_leading_ws=eat_leading_ws)
    self.text = text

  def __str__(self):
    return '<%s>' % self.text

  def initial(self):
    return self.text[0]

  def assign(self, obj, value):
    pass

  def parse(self, s):
    pos = 0
    if self.eat_leading_ws:
      while pos < len(s) and s[pos] == ' ':
        pos += 1
    if s[pos:].startswith(self.text):
      return (self.text, pos+len(self.text))
    raise Error('expected <%s>' % self.text, s)


def check_literal():
  try:
    a = Literal('foo')
    t, pos = a.parse('  foobar')
    assert t == 'foo'
    assert pos == 5
  except:
    raise e 

  try:
    a = Literal('foo', eat_leading_ws=False)
    t, pos = a.parse('  foobar')
    assert fail  # should not be here
  except Error as e:
    assert e.message.find('<foo>') > 0
    assert e.text == '  foobar'



class Number(FBase):

  def __init__(self, name, base=10, len=0, eat_leading_ws=True):
    super(Number, self).__init__(name=name, eat_leading_ws=eat_leading_ws)
    assert base in (8, 10, 16)
    self.base = base
    self.len = len
    self.eat_leading_ws = eat_leading_ws

  def __str__(self):
    if self.base == 10:
      return 'Number(%s)' % self.name
    return 'Number(%s,base=%d)' % (self.name, self.base)

  def initial(self):
    if self.base == 8:
      return '01234567'
    elif self.base == 10:
      return '0123456789'
    return '0123456789abcdef'

  def parse(self, s):
    pos = 0
    if self.eat_leading_ws:
      while pos < len(s) and s[pos] == ' ':
        pos += 1
    v = 0
    got = 0
    while pos < len(s):
      c = s[pos]
      oc = ord(c)
      idx = '0123456789abcdef'.find(c)
      if idx < 0:
        if got == 0 or (self.len > 0 and got < self.len):
          raise Error('%s: expect base %d number got char <%c>' % (self.name, self.base, c), s)
        break
      if idx >= self.base:
        break
      pos += 1
      got += 1
      # print(v, c, idx)
      v = v * self.base + idx

    return (v, pos)


def check_number():
  d = Number('foo')

  for s in [' 12', ' 12a', ' 12-']:
    n, pos = d.parse(s)
    # print(s, n, pos)
    assert n == 12
    assert pos == 3
    o = _Dummy()
    d.assign(o, n)
    assert o.foo == 12

  x = Number('foo', base=16)
  for s in [' 1f', ' 1fx', ' 1f-']:
    n, pos = x.parse(s)
    # print(s, n, pos)
    assert n == 31
    assert pos == 3

  try:
    a = Number('foo', base=8)
    t, pos = x.parse('128')
  except Error as e:
    assert e.message.find('base 8') > 0



class Text(FBase):

  def __init__(self, name, pattern=None, allow_space=False, eat_leading_ws=True,
               terminators=None):
    super(Text, self).__init__(name=name, eat_leading_ws=eat_leading_ws)
    self.pattern = pattern
    self.allow_space = allow_space
    self.eat_leading_ws = eat_leading_ws
    self.terminators = terminators

  def parse(self, s):
    pos = 0
    if self.eat_leading_ws:
      while pos < len(s) and s[pos] == ' ':
        pos += 1

    v = ''
    while pos < len(s):
      c = s[pos]
      if self.terminators and c in self.terminators:
        break
      if c == ' ' and not self.allow_space:
        pos += 1  # eat it, it's good for you
        break
      v += c
      pos += 1

    return (v, pos)



def check_text():
  foo = Text('foo')
  l1 = Literal(':')
  foo.terminators = l1.initial()
  bar = Text('bar')
  low = Number('low')
  l2 = Literal('-')
  high = Number('high')

  s = 'hello: test 42-55 or'
  pos = 0

  v, nxt = foo.parse(s[pos:])
  pos += nxt
  assert v == 'hello'

  v, nxt = l1.parse(s[pos:])
  pos += nxt

  v, nxt = bar.parse(s[pos:])
  pos += nxt
  assert v == 'test'

  v, nxt = low.parse(s[pos:])
  pos += nxt
  assert v == 42

  v, nxt = l2.parse(s[pos:])
  pos += nxt
  v, nxt = high.parse(s[pos:])
  pos += nxt
  assert v == 55


class QParser(object):

  def __init__(self, fields):
    self.fields = fields

    for fi in range(len(self.fields)):
      if self.fields[fi].__class__ == Text:
        if fi + 1 < len(self.fields):
          next = self.fields[fi+1]
          self.fields[fi].terminators = next.initial()

  def parse(self, o, text):
    pos = 0
    for fld in self.fields:
      v, nxt = fld.parse(text[pos:])
      pos += nxt
      fld.assign(o, v)

    pass


def check_parser():
  p = QParser([
      Text('name', allow_space=True),
      Literal(':'),
      Number('r1_low'),
      Literal('-'),
      Number('r1_high'),
      Literal('or'),
      Number('r2_low', base=16),
      Literal('-'),
      Number('r2_high', base=16),
      ])

  o = _Dummy()
  p.parse(o, 'arrival platform: 40-550 or 570-956')
  assert o.name == 'arrival platform'
  assert o.r1_low == 40
  assert o.r1_high == 550
  assert o.r2_low == 0x570
  assert o.r2_high == 0x956

  p.parse(o, 'class: 48-601 or ff-1ff\n')
  assert o.name == 'class'
  assert o.r1_low == 48
  assert o.r1_high == 601
  assert o.r2_low == 0xff
  assert o.r2_high == 0x1ff



def self_check():
  check_assignable()
  check_literal()
  check_number()
  check_text()
  check_parser()


if __name__ == '__main__':
  self_check()
  print('PASS:', __file__)
