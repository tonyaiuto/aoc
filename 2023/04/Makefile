
go:	bzl

bzl:	BUILD day04.bzl
	bazelisk build :all

BUILD:
	./to_build.sh <sample.txt >BUILD

watchbzl:
	../../tools/watch day04.bzl make --no-print-directory bzl


py:
	python3 day04.py

watchpy:
	../../tools/watch day04.py make --no-print-directory go


get:
	# mv $$HOME/Downloads/input.txt .
	curl -H "Cookie: $$(cat $$HOME/.cookie_aoc)" https://adventofcode.com/2023/day/4/input >input.txt
	chmod 444 input.txt
