
x:	t

p2:
	python day18.py -2 -v input.txt | tee part2.out

p1:
	python day18.py -v input.txt | grep -v time: | tee part1.out

t:
	python day18.py -v sample.txt | grep -v time: >sample.cur
	diff sample.out sample.cur
