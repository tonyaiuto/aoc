
sync:
	git fetch
	SYNCALL

all:
	(cd 2020 ; $(MAKE) -k$(MAKEFLAGS) all)
	(cd 2021 ; $(MAKE) -k$(MAKEFLAGS) all)
	(cd 2022 ; $(MAKE) -k$(MAKEFLAGS) all)
	(cd 2023 ; $(MAKE) -k$(MAKEFLAGS) all)
