"AOC 2020: day 6"

class Foo(object):

  def __init__(self):
    pass


  def __str__(self):
    return str(self)


def do_group_part1(group):
  # print('-------')
  all = set()
  for person in group:
    for q in person:
      all.add(q)
  # print(all)
  return len(all)

def do_group_part2(group):
  all = {}
  for person in group:
    for q in person:
      if not q in all:
        all[q] = 0
      all[q] += 1
  all_n = 0
  for q in all:
    if all[q] == len(group):
      all_n += 1
  return all_n

class day6(object):

  def __init__(self):
    pass

  def load(self, file):
    n_groups = 0
    sum_part1 = 0
    sum_part2 = 0
    with open(file, 'r') as inp:
      group = []
      n_groups += 1
      for line in inp:
        l = line.strip()
        if l:
          group.append(l)
        else:
          sum_part1 += do_group_part1(group)
          sum_part2 += do_group_part2(group)
          group = []
          n_groups += 1
      sum_part1 += do_group_part1(group)
      sum_part2 += do_group_part2(group)
    print(n_groups, 'groups')
    print('part1', sum_part1)
    print('part2', sum_part2)
    assert 7110 == sum_part1
    assert 3628 == sum_part2
   

  def part1(self):
    pass


def main(input):
  puzz = day6()
  puzz.load(input)
  puzz.part1()



if __name__ == '__main__':
  main('input.txt')
