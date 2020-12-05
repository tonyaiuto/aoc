

NROWS=127

class Foo(object):

  def __init__(self):
    pass


  def __str__(self):
    return str(self)


def pass_to_row(s):
  front = 0
  back = NROWS
  for i in range(7):
    half = s[i]
    nsize = int((back - front + 1) / 2)
    if half == 'F':
      back = front + nsize
    elif half == 'B':
      front = front + nsize
    # print(half, front, back)
  return front

assert pass_to_row('FBFBBFFRLR') == 44


SEAT_MAP = {
  'LLL': 0,
  'LLR': 1,
  'LRL': 2,
  'LRR': 3,
  'RLL': 4,
  'RLR': 5,
  'RRL': 6,
  'RRR': 7,
}

def pass_to_seat(s):
  row = pass_to_row(s)
  return row * 8 + SEAT_MAP[s[7:]]

assert pass_to_seat('FBFBBFFRLR') == 357
assert pass_to_seat('BFFFBBFRRR') == 567
assert pass_to_seat('FFFBBBFRRR') == 119
assert pass_to_seat('BBFFBBFRLL') == 820


def p2s(s):
  ret = 0
  for c in s:
    ret <<= 1
    if c in ('B', 'R'):
      ret |= 1
  return ret

assert p2s('FBFBBFFRLR') == 357
assert p2s('BFFFBBFRRR') == 567
assert p2s('FFFBBBFRRR') == 119
assert p2s('BBFFBBFRLL') == 820



class day5(object):

  def __init__(self):
    self.max_seat = 0
    self.occupied = set()

  def load(self, file):
    with open(file, 'r') as inp:
      for line in inp:
        l = line.strip()   
        seat = pass_to_seat(l)
        self.occupied.add(seat)
        self.max_seat = max(self.max_seat, seat)

  def part1(self):
    print('part1', self.max_seat)

  def part2(self):
    for i in range(self.max_seat):
      if i not in self.occupied:
        print('vacant', i)



def main(input):
  puzz = day5()
  puzz.load(input)
  puzz.part1()
  puzz.part2()


if __name__ == '__main__':
  main('input.txt')
