
go:	reader_test prog_test

reader_test:
	python3 reader.py

prog_test:
	sed -e "s/@N@/_test/g" prog.py >prog_test.py
	python3 prog_test.py
