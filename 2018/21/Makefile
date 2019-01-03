

p2:	part2
	./part2 | sed -n -e 's/done: i_count=//p' | sort -n | tail -5

p2x:
	./part2 | head -100000 >6
	diff 5 6

p1:	part1
	./part1

tp2:	p1 part1
	./p1 | head -100000 >/tmp/p1.out
	./part1 | head -100000 >/tmp/p2.out
	diff /tmp/p1.out /tmp/p2.out

p1_base:	p1.c p1.inc
	$(CC) -o $@ p1.c

p1.inc:	input.txt day21.py Makefile
	python day21.py input.txt >$@

