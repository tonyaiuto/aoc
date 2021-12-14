C AOC 2021 Day 13
       program main

       integer x(0:1000), y(0:1000)
       character*1 fold_dir(100)
       integer fold_pos(100)
       integer n_dots, n_folds

       integer err
       character*20 junk, junk2, rest

       open(unit=10, file='dots.txt')
       n_dots = 0
       err = 0
       do while (err .eq. 0)
         read(10, *, iostat=err) x(n_dots), y(n_dots)
         n_dots = n_dots + 1
       end do
       n_dots = n_dots - 1
C      call print_dots(x, y, n_dots)

       open(unit=11, file='folds.txt')
       n_folds = 0
       err = 0
       do while (err .eq. 0)
         read(11, *, iostat=err) junk, junk2, rest
         if (err == 0) then
           n_folds = n_folds + 1
           fold_dir(n_folds) = rest(1:1)
           n = 0 
           do i = 3,20
             j = ichar(rest(i:i))
             if (j >= 48 .and. j <= 58) then
               n = n * 10 + ichar(rest(i:i)) - 48
             end if
           end do
           fold_pos(n_folds) = n
         end if
       end do
C      write(6, *) n_folds
C      do i = 1, n_folds
C        write(6, *) fold_dir(i), fold_pos(i)
C      end do

C      call part1(x, y, n_dots, fold_dir, fold_pos, n_folds)
C      write(6, *) 'part1:', n_dots
       call part2(x, y, n_dots, fold_dir, fold_pos, n_folds)
       end

       subroutine  print_dots(x, y, n_dots)
         integer x(0:1), y(0:1), n_dots
         write(6, *) 'Dots:', n_dots
         do i = 0, n_dots-1
           write(6, *) i, x(i), y(i)
         end do
       end


       subroutine part1(x, y, n_dots, fold_dir, fold_pos, n_folds)
         integer x(0:1), y(0:1), fold_pos(1)
         character*1 fold_dir(1)
         call fold(x, y, n_dots, fold_dir(1), fold_pos(1))
       end


       subroutine fold(x, y, n_dots, fold_dir, fold_pos)
         integer x(0:1), y(0:1), fold_pos
         character*1 fold_dir
         if (fold_dir .eq. 'x') then
           do i = 0, n_dots-1
             if (x(i) .gt. fold_pos) then
               x(i) = fold_pos*2 - x(i)
             end if
           end do
         else
           do i = 0, n_dots-1
             if (y(i) .gt. fold_pos) then
               y(i) = fold_pos*2 - y(i)
             end if
           end do
         end if
C        call print_dots(x, y, n_dots)
       end

       subroutine part2(x, y, n_dots, fold_dir, fold_pos, n_folds)
         integer x(0:1), y(0:1), fold_pos(1)
         character*1 fold_dir(1)
         character*50 disp(0:7)

         do ifold = 1, n_folds
           call fold(x, y, n_dots, fold_dir(ifold), fold_pos(ifold))
         end do

C        Convert dots to image
         do j_row = 0, 7
           disp(j_row) = ' '
         end do
         do i_dot = 0, n_dots - 1
          ix = x(i_dot) + 1
           disp(y(i_dot))(ix:ix) = '#'
         end do
         do i_row = 0, 7
           write(6, *) disp(i_row)
         end do
       end

