#!/bin/bash

if [[ $# -ne 1 ]] ; then
  echo 'usage: newday.sh N'
  exit 1
fi

day=$(printf %d $1)
day2=$(printf %02d $1)
year=$(date +%Y)
if [[ -d $day2 ]] ; then
  echo "$day2 exists"
  exit 1
fi
  
mkdir $day2
sed -e "s/@YEAR@/$year/g" -e "s/@N@/$day/g" -e "s/@N2@/${day2}/g" ../tmpl/Makefile.tmpl >$day2/Makefile
sed -e "s/@YEAR@/$year/g" -e "s/@N@/$day/g" -e "s/@N2@/${day2}/g" ../tmpl/prog.py >$day2/day${day2}.py
(cd $day2 ; ln -s ../../tools ; chmod a+x *.py)
