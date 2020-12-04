

class ConstrainedValue(object):

  def __init__(self, name, typ=None, length=0, mask=None, low=-1, high=-1, enum=None):
    self.name = name
    self.typ = typ
    self.length = length
    self.mask = mask
    self.low = low
    self.high = high
    self.enum = enum
    if low >= 0:
      if not typ:
        self.typ = int
    self._ok = -1
    self._v = None

  def set(self, s):
    self._v = s
    if self.length > 0 and self.length != len(s):
      print('bad length:', self.name, 'expect', self.length, 'got', len(s), s)
      self._ok = 0
    if self.mask:
      if len(self.mask) != len(s):
        print('bad mask length:', self.name, 'expect', len(self.mask), 'got', len(s), s)
        self._ok = 0
      else:
        self._ok = 1
        for i in range(len(self.mask)):
          expect = self.mask[i]
          got = s[i]
          if expect == 'd':
            if not got.isdigit():
              print('mask fail D ', i, expect, got, self.mask, s)
              self._ok = 0
          elif expect == 'x':
            if not (got.isdigit() or (got >= 'a' and got <= 'f')):
              print('mask fail X ', i, expect, got, self.mask, s)
              self._ok = 0
          elif expect != got:
            print('mask fail OTHER ', i, expect, got, self.mask, s)
            self._ok = 0

    elif self.enum:
      if s not in self.enum:
        print('bad enum:', self.name, s, self.enum)
        self._ok = 0
      else:
        self._ok = 1

    elif self.low >= 0:
      self._v = self.typ(s)
      if self._v < self.low or self._v > self.high:
        print('bad range:', self.name, self.low, '<=', s, '<=', self.high)
        self._ok = 0
      else:
        self._ok = 1

    return self._ok == 1

  @property
  def ok(self):
    return self._ok == 1

  @property
  def unset(self):
    return self._ok == -1

  @property
  def v(self):
    return self.v


class Passport(object):

  FIELD_NAMES = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')

  def __init__(self, id='?'):
    self.id = id
    self.fields = {}
    self.invalid = False
    self.byr = ConstrainedValue('byr', typ=int, length=4, low=1920, high=2002)
    self.iyr = ConstrainedValue('iyr', typ=int, length=4, low=2010, high=2020)
    self.eyr = ConstrainedValue('eyr', typ=int, length=4, low=2020, high=2030)
    self.hcl = ConstrainedValue('hcl', typ=str, mask='#xxxxxx')
    self.ecl = ConstrainedValue('ecl', typ=str,
                                enum=('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'))
    self.pid = ConstrainedValue('pid', typ=str, mask='ddddddddd')

  def add_fields(self, text):
      for fld in text.split(' '):
        try:
          field, value = fld.split(':')
        except Exception as e:
          print('bad parse', text, e)
        self.add_field(field, value)

  def add_field(self, field, value):
    # print(field, value)
    if field not in Passport.FIELD_NAMES:
      print('illegal field:', field, text)
      self.invalid = True
      return

    if field in self.fields:
      print('Duplicate', field, text)
      self.invalid = True
      return
    assert field not in self.fields

    self.fields[field] = value

    if field == 'byr':
      if not self.byr.set(value):
        self.invalid = True

    elif field == 'iyr':
      if not self.iyr.set(value):
        self.invalid = True

    elif field == 'eyr':
      if not self.eyr.set(value):
        self.invalid = True

    elif field == 'hgt':
      if value and value.endswith('cm'):
        n = int(value[0:-2])
        if n < 150 or n > 193:
          self.invalid = True
      elif value and value.endswith('in'):
        n = int(value[0:-2])
        if n < 59 or n > 76:
          self.invalid = True
      else:
        print('bad hgt', value, self.fields)
        self.invalid = True

    elif field == 'hcl':
      if not self.hcl.set(value):
        self.invalid = True

    elif field == 'ecl':
      if not self.ecl.set(value):
        self.invalid = True

    elif field == 'pid':
      if not self.pid.set(value):
        self.invalid = True


  def v(self, fld):
    v = self.fields.get(fld)
    if not v:
      print("missing", fld)
    return v

  def is_valid(self):
    if len(self.fields) < 7:
      return False
    if len(self.fields) == 7 and 'cid' in self.fields:
      return False
    #if self.invalid:
    #  print('  invalid:', self.fields)
    return not self.invalid


class day4(object):

  def __init__(self):
    pass

  def load(self, file):
    n = 0
    n_valid = 0
    cur_pass = Passport(n)
    with open(file, 'r') as inp:
      for line in inp:
        l = line.strip()
        if not l:
          n += 1
          if cur_pass.is_valid():
            n_valid += 1
            print('== ok', n, n_valid)
          else:
            print('== bad', n, n_valid, cur_pass.fields)
          cur_pass = Passport(n)
          print('=====', n, n_valid)
        else:
          cur_pass.add_fields(l)
    print(cur_pass.fields)
    if cur_pass.is_valid():
      n_valid += 1
    print('part2', n_valid)



def main(input):
  puzz = day4()
  puzz.load(input)


if __name__ == '__main__':
  main('input.txt')
