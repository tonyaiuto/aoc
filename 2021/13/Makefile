
go:
	python3 day13.py
	@echo


watch:
	../../tools/watch day13.py make --no-print-directory go


get:
	# mv $$HOME/Downloads/input.txt .
	curl -H "Cookie: $$(cat $$HOME/.cookie_aoc)" https://adventofcode.com/2021/day/13/input >input.txt
	chmod 444 input.txt


day13_f:	day13.f
	f77 -o $@ day13.f

fort:	day13_f 
	cd 1 ; ../day13_f dots.txt fold.txt
	cd 2 ; ../day13_f dots.txt fold.txt

