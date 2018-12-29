

x:	p2c


part1:	input.txt
	python day19.py -v input.txt >/tmp/run.out

part2:	input.txt
	python day19.py -2 input.txt >/tmp/run.out

p2c:	day19
	./day19 22 >part2.out

t:	sample.txt sample.out
	python day19.py -v sample.txt >/tmp/run.out
	diff sample.out /tmp/run.out
