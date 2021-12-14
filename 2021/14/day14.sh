#!/bin/bash

poly=$(head -1 input.txt)

echo 
echo "Starting day at $(date)"

declare -A lcount

declare -A rules
tmp=$(mktemp)
# Believe it or not  rules[$pair]=$rep does not quite work.
( sed -n -e '/->/s/ ->//p' input.txt | while read pair rep ; do
echo rules[$pair]=$rep
done
) >$tmp
source $tmp
rm -f $tmp

# echo ${rules[@]}

inc_letter() {
  if [[ -z "${lcount[$1]}" ]] ; then
    lcount[$1]=$2
  else
    lcount[$1]=$(expr ${lcount[$1]} + $2)
  fi
  # echo "inc_letter $1 $2 -> ${lcount[$1]}"
}

declare -A pair_counts
inc_pair() {
  if [[ -z "${pair_counts[$1]}" ]] ; then
    pair_counts[$1]=$2
  else
    pair_counts[$1]=$(expr ${pair_counts[$1]} + $2)
  fi
}

pairs() {
  prev=''
  for letter in $(echo $1 | grep -o .) ; do
    if [[ -n "$prev" ]] ; then
      echo "$prev$letter"
    fi
    prev=$letter
  done
}

# count the letters already there
for letter in $(echo $poly | grep -o .) ; do
  inc_letter $letter 1
done
echo ${lcount[@]}

# count the pairs
for pair in $(pairs $poly) ; do
  inc_pair $pair 1
done

echo ${!pair_counts[@]}
echo ${pair_counts[@]}

inc_tmp() {
  if [[ -z "${tmp[$1]}" ]] ; then
    tmp[$1]=$2
  else
    tmp[$1]=$(expr ${tmp[$1]} + $2)
  fi
}

do_gen() {
  for p in ${!pair_counts[@]} ; do
    rep=${rules[$p]}
    inc=${pair_counts[$p]}
    # echo "doing $p" $rep $inc
    if [[ -n "$rep" ]] ; then
      inc_letter $rep $inc
      set $(echo $p | sed -e 's/^\(.\)/\1 /')
      inc_tmp "$1$rep" $inc
      inc_tmp "$rep$2" $inc
    fi
  done
}  

# echo ${rules[*]}

i=0
while [[ $i -lt 40 ]] ; do
  i=$(expr $i + 1)
  echo Loop $i $(date +' at %H:%M:%S')
  unset tmp
  declare -A tmp
  do_gen
  unset pair_counts
  declare -A pair_counts
  for key in ${!tmp[@]} ; do
    pair_counts[$key]=${tmp[$key]}
  done
  pair_counts=$tmp
  # echo ${!pair_counts[@]}
  # echo ${pair_counts[@]}
done

# (for count in ${lcount[@]} ; do echo $count ; done) | sort -n
high=$((for count in ${lcount[@]} ; do echo $count ; done) | sort -n | tail -1)
low=$((for count in ${lcount[@]} ; do echo $count ; done) | sort -n | head -1)
expr $high - $low

exit 0
