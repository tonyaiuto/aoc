

x:	t1

# expect 31891
part1:	input.txt
	python day17.py -v input.txt | tee /tmp/run.out


part2:	input.txt
	python day17.py -v -2 input.txt | tee /tmp/run.out
        grep wells /tmp/run.out
	echo expect: 24927 tiles are in wells


t1:	sample.txt
	python day17.py -v sample.txt > /tmp/run.out
	diff sample.out /tmp/run.out
