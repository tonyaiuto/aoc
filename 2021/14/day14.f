C AOC 2021 Day 14
       program main

       character*1 line(80), c
       integer err

       integer template(80)
C      rules
       integer reps(26, 26)
       integer*8 cnts(26, 26)
C      how many of each
       integer*8 letter_counts(26)

       letter_counts = 0
       reps = 0
       cnts = 0

C      read tempalte
       open(unit=10, file='input.txt')
       read(10, fmt='(80A1)', iostat=err) line
       do i = 1, 80
         let = ichar(line(i))
         if (let .gt. 64) then
           template(i) = let - 64
         else
           template(i) = -1
         end if
       end do
C      write(6, fmt='(10I3)') (template(i), i=1,10)
       do i = 1, 80
         k = template(i)
         if (k .gt. 0) then
           letter_counts(k) = letter_counts(k) + 1
         end if
       end do

C      skip blank
       read(10, fmt='(80A1)', iostat=err) line

C      read rules
       err = 0
       do while (err .eq. 0)
         read(10, fmt='(80A1)', iostat=err) line
         if (err .eq. 0) then
           n1 = ichar(line(1)) - 64
           n2 = ichar(line(2)) - 64
           i = n1 * 26 + n2
           reps(n1, n2) = ichar(line(7)) - 64
	   c = char(reps(n1, n2)+64)
C          write(6, *) n1, n2, reps(n1, n2), char(n1+64), char(n2+64), c
         end if
       end do
C      call print_rules(reps, cnts) 

C      Count the pairs to prime the pump
       i_p = -1
       do i = 1, 60
         k = template(i)
         if (k .gt. 0 .and. i_p .gt. 0) then
            cnts(i_p, k) = cnts(i_p, k) + 1
         end if
         i_p = k
       end do

       call part1(template, reps, cnts, letter_counts)
C      write(6, *) 'part1:', n_dots
C      call part2(x, y, n_dots, fold_dir, fold_pos, n_folds)
       end

       subroutine print_rules(reps, cnts)
         integer reps(26, 26)
         integer*8 cnts(26, 26)

         integer i, j
         character*1 c

         do i = 1, 26
           do j = 1, 26
             if (reps(i, j) .gt. 0) then
               c = char(reps(i, j) + 64)
               write(6, *) char(i + 64), char(j + 64), reps(i, j), c
             end if
           end do
         end do
       end

       subroutine iscore(letter_counts, ret)
         integer*8 letter_counts(26)
         integer*8 ret

         integer*8 min_c, max_c

         max_c = 0
         min_c = -1
         do l = 1, 26
           if (letter_counts(l) .gt. 0) then
             if (letter_counts(l) .lt. min_c .or. min_c .eq. -1) then
               min_c = letter_counts(l)
             end if
             if (letter_counts(l) .gt. max_c) then
               max_c = letter_counts(l)
             end if
           end if
C          write(6, *) char(l+64), letter_counts(l), min_c, max_c
         end do
         ret = max_c - min_c
       end

       subroutine part1(template, reps, cnts, letter_counts)
         integer template(80)
         integer reps(26, 26)
         integer*8 cnts(26, 26)
         integer*8 letter_counts(26)
         integer*8 score

         do i = 1, 40 
           call do_gen(cnts, reps, letter_counts)
         end do
         call iscore(letter_counts, score)
         write(6, *) 'score', score
       end

       subroutine do_gen(cnts, reps, letter_counts)
         integer*8 cnts(26, 26)
         integer reps(26, 26)
         integer*8 letter_counts(26)

         integer*8 ret(26, 26)
         integer rep

         ret = 0
         do i = 1, 26
           do j = 1, 26
             rep = reps(i, j)
             if (rep .gt. 0) then
               n1 = i / 26
               n2 = mod(i, 26)
               letter_counts(rep) = letter_counts(rep) + cnts(i, j)
               ret(i, rep) = ret(i, rep) + cnts(i, j)
               ret(rep, j) = ret(rep, j) + cnts(i, j)
             end if
           end do
         end do
         cnts = ret
       end
