
go:
	python3 day05.py
	@echo

watch:
	../../tools/watch day05.py make --no-print-directory go

get:
	# mv $$HOME/Downloads/input.txt .
	curl -H "Cookie: $$(cat $$HOME/.cookie_aoc)" https://adventofcode.com/2023/day/5/input >input.txt
	chmod 444 input.txt
