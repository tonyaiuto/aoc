#!/bin/bash

if [[ $# -ne 1 ]] ; then
  echo 'usage: newday.sh N'
  exit 1
fi

day=$1
if [[ -d $day ]] ; then
  echo "$day exists"
  exit 1
fi
  
mkdir $day
sed -e "s/@N@/$day/g" tmpl/Makefile.tmpl >$day/Makefile
sed -e "s/@N@/$day/g" tmpl/prog.py >$day/day${day}.py
(cd $day ; ln -s ../../tools/memoized.py)
(cd $day ; ln -s ../../tools/reader.py)
