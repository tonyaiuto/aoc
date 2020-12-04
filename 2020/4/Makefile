
go:
	python3 day4.py


cmp:
	python3 day4.py | grep '^== ok' >out.1
	python3 day4_alt.py | grep '^== ok' >out.2
	python3 day4.py | grep '^== bad' >bad.1
	python3 day4_alt.py | grep '^== bad' >bad.2
	diff out.1 out.2
