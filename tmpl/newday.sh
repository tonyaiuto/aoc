#!/bin/bash

if [[ $# -ne 1 ]] ; then
  echo 'usage: newday.sh N'
  exit 1
fi

day=$(printf %d $1)
day2=$(printf %02d $1)
year=$(date +%Y)
if [[ -d $day2 ]] ; then
  echo "$day2 exists.  refreshing"
fi
  
mkdir -p $day2
if [[ ! -f $day2/Makefile ]] ; then
  sed -e "s/@YEAR@/$year/g" -e "s/@N@/$day/g" -e "s/@N2@/${day2}/g" ../tmpl/Makefile.tmpl >$day2/Makefile
fi
if [[ ! -f $day2/day${day2}.py ]] ; then
  sed -e "s/@YEAR@/$year/g" -e "s/@N@/$day/g" -e "s/@N2@/${day2}/g" ../tmpl/prog.py >$day2/day${day2}.py
fi

cd $day2
ln -s ../../tools
chmod a+x *.py
if [[ ! -d ../../input/$year/$day2 ]] ; then
  mkdir ../../input/$year/$day2
  touch ../../input/$year/$day2/input.txt
fi
ln -s ../../input/$year/$day2/input.txt
