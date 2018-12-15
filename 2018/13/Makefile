

part2:
	python day13.py -2 input.txt | tee part2.out

part1:
	python day13.py input.txt | tee part1.out

test:	t t2

t:
	- python day13.py -v sample.txt >sample.cur
	diff sample.out sample.cur

t2:
	- python day13.py -v -2 sample2.txt >sample.cur
	diff sample2.out sample.cur
