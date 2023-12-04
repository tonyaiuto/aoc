#!/bin/bash -e

# Convert day4 input into BUILD format

echo 'load(":day04.bzl", "card")'
sed -e 's/  */ /g' \
    -e 's/^Card *\([0-9]*\): */card(name="\1", winners=[/' \
    -e 's/\([0-9][0-9]*\) /\1,/g' \
    -e 's/|/], got=[/' \
    -e 's/$/])/' |
sed -e '$s/)/, out="part2.txt")/'
