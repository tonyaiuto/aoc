

def part1(inp_file):
  sum = 0
  with open(inp_file, 'r') as inp:
    for line in inp:
      first = -1
      for c in line:
        if c.isdigit():
          d = ord(c) - ord('0')
          if first < 0:
            first = d
          last = d
      v = first * 10 + last
      # print(line, '=>', v)
      sum += v
  print("sum", inp_file, sum)

NUMBERS = [
        # ['zero', '0'],
        ['one', '1'],
        ['two', '2'],
        ['three', '3'],
        ['four', '4'],
        ['five', '5'],
        ['six', '6'],
        ['seven', '7'],
        ['eight', '8'],
        ['nine', '9'],
]

def to_digit(s):
  for n in NUMBERS:
    if s.startswith(n[0]):
      return len(n[0]), n[1]
  return 1, ''

def part2(inp_file):
  sum = 0
  with open(inp_file, 'r') as inp:
    for line in inp:
      i = 0
      first = -1
      last = 'unset'
      while i < len(line):
        inc, c = to_digit(line[i:])
        if inc == 1:
          c = line[i]
        i += inc
        if c.isdigit():
          first = ord(c) - ord('0')
          #if first < 0:
          #  first = d
          #last = d
          break

      i = len(line) - 1
      while i >= 0:
        inc, c = to_digit(line[i:])
        if inc == 1:
          c = line[i]
        i -= 1
        if c.isdigit():
          last = ord(c) - ord('0')
          break

      i = len(line) - 1
      while i > 0:
        inc, c = to_digit(line[i:])
        if inc == 1:
          c = line[i]
        i -= 1
        if c.isdigit():
          last2 = ord(c) - ord('0')
          break
      if last != last2:
        print("GOT IT", line, last, last2)
        # return -1

      v = first * 10 + last
      # print(line.strip(), '=>', v)
      sum += v
  print("sum", inp_file, sum)
  return sum

part1('input.txt')

v = part2('sample.txt')
assert v == 281
part2('input.txt')
