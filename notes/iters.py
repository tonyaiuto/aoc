
import itertools

for x,y,z in itertools.product(range(2), range(3), range(4)):
  print(x, y, z)

print('xxxxxxxxxxxx')
for x in itertools.product(range(2), repeat=4):
  print(x)

