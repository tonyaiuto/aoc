

x:	inp
	python day7.py inp


inp:	input.txt Makefile
	sed -e 's/^Step //' -e 's/must.*step//' \
		-e 's/ can beg.*$$//' -e 's/  / /g' input.txt >$@
