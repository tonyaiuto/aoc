
part1:
	python day20.py input.txt
	@echo Furthest room requires passing 4121 doors

part2:
	echo TOO LOW: 3122 rooms, max path=4121
	echo TOO LOW: 7883 rooms, max path=4121
	echo TOO HIGH: 9725 rooms, max path=4121


test_part1:
	python day20.py -e '^WNE$$'
	@echo Furthest room requires passing 3 doors
	python day20.py -e '^ENWWW(NEEE|SSE(EE|N))$$'
	@echo Furthest room requires passing 10 doors
	python day20.py -e '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$$'
	@echo Furthest room requires passing 18 doors
	python day20.py -e '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$$'
	@echo Furthest room requires passing 23 doors
	python day20.py sample1.txt >/tmp/test_part1.out
	python day20.py sample2.txt >>/tmp/test_part1.out
	python day20.py sample3.txt >>/tmp/test_part1.out
	python day20.py sample4.txt >>/tmp/test_part1.out
	grep requires sample*.out | diff -- - /tmp/test_part1.out

test_parse:
	python day20.py -d input.txt >/tmp/input.parsed
	diff input.txt /tmp/input.parsed
