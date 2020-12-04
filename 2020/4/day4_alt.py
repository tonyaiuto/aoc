
class Passport(object):

  FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')

  def __init__(self):
    self.fields = {}
    self.invalid = False

  def add_fields(self, text):
    try:
      for fld in text.split(' '):
        field, value = fld.split(':')
        self.add_field(field, value)
    except:
      print('bad parse', text)

  def add_field(self, field, value):
    # print(field, value)
    if field not in Passport.FIELDS:
      print('illegal field:', field, text)
      self.invalid = True
      return

    if field in self.fields:
      print('Duplicate', field, text)
      self.invalid = True
      return

    self.fields[field] = value
   
    if field == 'byr':
      n = int(value)
      if n < 1920 or n > 2002:
        self.invalid = True

    elif field == 'iyr':
      n = int(value)
      if n < 2010 or n > 2020:
        self.invalid = True

    elif field == 'eyr':
      n = int(value)
      if n < 2020 or n > 2030:
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


  def v(self, fld):
    v = self.fields.get(fld)
    if not v:
      print("missing", fld)
    return v

  def is_valid(self):
    if len(self.fields) < 7:
      return False

    if self.invalid:
      return False

    v = self.v('hcl')
    if not v:
      return False
    if len(v) != 7:
      return False
    if v[0] != '#':
      return False
    for c in v[1:]:
      if c not in '0123456789abcdef':
        return False
    print('good hcl', v)

    v = self.v('ecl')
    if v not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
      print('bad ecl', v)
      return False

    v = self.v('pid')
    if not v:
      return False
    if len(v) != 9:
      print('short pid', v)
      return False
    for c in v:
      if c not in '0123456789':
        return False
    print('pid', v)

    return True


class day4(object):

  def __init__(self):
    pass

  def load(self, file):
    n_valid = 0
    cur_pass = Passport()
    with open(file, 'r') as inp:
      for line in inp:
        l = line.strip()   
        if not l:
          if cur_pass.is_valid():
            n_valid += 1
          # print(cur_pass.fields)
          cur_pass = Passport()
        else:
          cur_pass.add_fields(l)
    print(cur_pass.fields)
    if cur_pass.is_valid():
      n_valid += 1
    print('part1', n_valid)



def main(input):
  puzz = day4()
  puzz.load(input)


if __name__ == '__main__':
  main('input.txt')
