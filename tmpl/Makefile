
go:	prog_test

prog_test:
	- ln -s ../tools .
	sed \
	  -e "s/@N2@/_test/g" \
	  -e "s/expect1=None/expect1=42/g" \
	  -e "s/expect2=None/expect2=42/g" \
	  prog.py >prog_test.py
	python3 prog_test.py
