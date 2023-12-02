
go:
	python3 day01.py
	@echo


watch:
	../../tools/watch day01.py make --no-print-directory go


get:
	# mv $$HOME/Downloads/input.txt .
	curl -H "Cookie: $$(cat $$HOME/.cookie_aoc)" https://adventofcode.com/2022/day/1/input >input.txt
	chmod 444 input.txt
