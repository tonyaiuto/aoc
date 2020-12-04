

class Passport(object):

  FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')

  def __init__(self): self.fields = {}

  def add_fields(self, text):
    try:
      for fld in text.split(' '):
        fname, value = fld.split(':')
        # print(fname, value)
        if fname in Passport.FIELDS:
          if fname in self.fields:
            print('Duplicate', fname, text)
          self.fields[fname] = value
        else:
          print('illegal field:', fname, text)
    except:
      print(text)

  def v(self, fld):
    v = self.fields.get(fld)
    if not v:
      print("missing", fld)
    return v

  @property
  def byr(self):
    v = self.fields.get('byr')
    if not v:
      return -1 
    if len(v) != 4:
      print("bad year", v)
      return -1
    return int(v)

  @property
  def eyr(self):
    v = self.fields.get('eyr')
    if not v:
      return 0
    if len(v) != 4:
      print("bad year", v)
      return -1
    return int(v)

  @property
  def iyr(self):
    v = self.fields.get('iyr')
    if not v:
      return 0
    if len(v) != 4:
      print("bad year", v)
      return -1
    return int(v)

  def is_valid(self):
    if len(self.fields) < 7:
      return False

    if self.byr < 1920 or self.byr > 2002:
      print('byr', self.byr)
      return False

    if self.iyr < 2010 or self.iyr > 2020:
      return False

    if self.eyr < 2020 or self.eyr > 2030:
      return False

    v = self.v('hgt')
    if not v:
      return False
    if v and v.endswith('cm'):
      n = int(v[0:-2])
      if n < 150 or n > 193:
        return False
    elif v and v.endswith('in'):
      n = int(v[0:-2])
      if n < 59 or n > 76:
        return False
    else:
      print('bad hgt', self.fields)
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
