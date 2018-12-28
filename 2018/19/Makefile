

x:	t

part1:	input.txt
	python day19.py -v input.txt >/tmp/run.out

part2:	input.txt
	python day19.py -v -2 input.txt >/tmp/run.out

t:	sample.txt sample.out
	python day19.py -v sample.txt >/tmp/run.out
	diff sample.out /tmp/run.out
