
go:
	python3 day03.py
	@echo


watch:
	../../tools/watch day03.py make --no-print-directory go


get:
	# mv $$HOME/Downloads/input.txt .
	curl -H "Cookie: $$(cat $$HOME/.cookie_aoc)" https://adventofcode.com/2024/day/3/input >input.txt
	chmod 444 input.txt


alt:	Makefile
	(echo -n inp='"""' ; sed -e 's/)/)|/g' input.txt ; echo '"""' ) >ii.py
	echo 'for x in inp.split("|"):' >>ii.py
	echo '  print(x)' >>ii.py
	python3 ii.py  | sed -n -e 's/^.*mul(/mul(/p' | grep ')$$' > m1
	grep -v '[- abcdefghijknopqrstvwxyz!#]' m1 >m2
	sed -e 's/mul(/expr /' -e 's/,/ \\* /' -e 's/)//' m2 >m3.sh
	python3 chk.py
