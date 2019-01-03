

x:	part1
	./part1

tp2:	p1 part1
	./p1 | head -100000 >/tmp/p1.out
	./part1 | head -100000 >/tmp/p2.out
	diff /tmp/p1.out /tmp/p2.out

p1:	p1.c p1.inc
	$(CC) -o $@ p1.c

p1.inc:	input.txt day21.py Makefile
	python day21.py input.txt >$@

part2:	input.txt
	python day21.py -2 input.txt >/tmp/run.out

p2c:	day21
	./day21 22 >part2.out

t:	sample.txt sample.out
	python day21.py -v sample.txt >/tmp/run.out
	diff sample.out /tmp/run.out
