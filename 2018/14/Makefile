
g:	t2

part2:
	- python day14.py -2 37 509671

part1:
	python day14.py 37 509671 | tee part1.out

test:	t t2

t:
	- python day14.py -v 37 2018 >sample.cur
	diff sample.out sample.cur

t2:
	- python day14.py -2 37 51589 # first appears after 9 recipes.
	- python day14.py -2 37 01245 # first appears after 5 recipes.
	- python day14.py -2 37 92510 # first appears after 18 recipes.
	- python day14.py -2 37 59414 # first appears after 2018 recipes.
	echo 509671 appears after 583607528

