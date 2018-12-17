

x:	t2

part2:
	python day13.py -2 input.txt | tee part2.out

part1:
	python day15.py input.txt | tee part1.out

test:
	rm sample*.out sample*.cur
	$(MAKE) -$(MAKEFLAGS) sample.out sample2.out sample3.out sample4.out
	$(MAKE) -$(MAKEFLAGS) sample.cur sample2.cur sample3.cur sample4.cur

tpart2:
	python day15.py -v -2 sample.txt >sample.cur
	diff -w sample_part2.out sample.cur

t1:	sample.txt sample.out
	python day15.py -v sample.txt >/tmp/run.out
	grep -v '^ *=' /tmp/run.out >sample.cur
	diff -w sample.out sample.cur

t2:	sample2.txt sample2.out
	python day15.py -v sample2.txt >/tmp/run.out
	grep -v '^ *=' /tmp/run.out >sample2.cur
	diff -w sample2.out sample2.cur

.SUFFIXES:	.out .txt .cur

.txt.out:
	sed -e '/lim/,/= expect/d' \
	    -e '/^\/\//d' \
	    -e 's/  */ /g' \
	    -e 's/),/)/g' $? >$@

.txt.cur:
	python day15.py -v $? | tee /tmp/run.out | grep -v '^ *=' >$@
	diff -w $*.out $*.cur
