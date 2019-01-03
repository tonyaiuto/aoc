
#include <stdio.h>

int r0, r1, r2, r4, r5;

void preg(int l) {
  printf("%2d: %6d %6d %6d pc %6d %6d\n", l, r0, r1, r2, r4, r5);
}


// int r0, r1, r2, r4, r5;

int prog() {
  while (1) {
    r4 = 123;                      // seti 123 0 4
    r4 = r4 & 456;                 // bani 4 456 4
    r4 = r4 == 72;                 // eqri 4 72 4
    if (r4) break;
    preg(4);
    return -1;
  }

  r4 = 0;                        // seti 0 6 4
  while(1) {
    r5 = r4 | 0x10000;               // bori 4 65536 5
    r4 = 1855046;                  // seti 1855046 9 4
    // hex(1855046) = '0x1c4e46'

    while(1) {
      r2 = r5 & 0xff;                 // bani 5 255 2
      r4 = r4 + r2;                  // addr 4 2 4
      // clip to 24 bits
      r4 = r4 & 0xffffff;            // bani 4 16777215 4
      r4 = r4 * 65899;               // muli 4 65899 4
      r4 = r4 & 0xffffff;            // bani 4 16777215 4
      r2 = 256 > r5;                 // gtir 256 5 2
      if (r2) break;              // addr 2 3 3

#if 0
      r2 = 0;                        // seti 0 9 2
      // preg(26);
      while(1) {
	    r1 = r2 + 1;                   // addi 2 1 1
	    r1 = r1 * 256;                 // muli 1 256 1
	    r1 = r1 > r5;                  // gtrr 1 5 1
	    if (r1) break;              // addr 1 3 3
	    r2 = r2 + 1;                   // addi 2 1 2
	    preg(25);
      }
      r5 = r2;                       // setr 2 7 5
      preg(27);
#else
      r2 = r5 / 256;                       // setr 2 7 5
      r5 = r2;
#endif
    }

    r2 = r4 == r0;                 // eqrr 4 0 2
    if (r2) break;              // addr 2 3 3
    preg(30);
  }
  return 0;
}

int main(int argc, char *argv[]) {
  r0 = r1 = r2 = r4 = r5 = 0;
  prog();
}
/*
26:      0      0      0 pc 6880578  65536
27:      0      1    256 pc 6880578    256
26:      0      1      0 pc 2170006    256
27:      0      1      1 pc 2170006      1
30:      0      1      0 pc 9079325      1
26:      0      1      0 pc 8791649 9144861
27:      0      1  35722 pc 8791649  35722
26:      0      1      0 pc 2371385  35722
27:      0      1    139 pc 2371385    139
30:      0      1      0 pc 1293036    139
26:      0      1      0 pc 5655526 1293036
27:      0      1   5050 pc 5655526   5050
26:      0      1      0 pc 16688864   5050
27:      0      1     19 pc 16688864     19
30:      0      1      0 pc 637585     19
26:      0      1      0 pc 16435933 637585
27:      0      1   2490 pc 16435933   2490
26:      0      1      0 pc 3518237   2490
27:      0      1      9 pc 3518237      9
30:      0      1      0 pc 4545250      9
26:      0      1      0 pc 4996536 4545250
27:      0      1  17754 pc 4996536  17754
26:      0      1      0 pc 3015558  17754
27:      0      1     69 pc 3015558     69
30:      0      1      0 pc 680153     69
26:      0      1      0 pc 4403445 745689
27:      0      1   2912 pc 4403445   2912
26:      0      1      0 pc 10220423   2912
27:      0      1     11 pc 10220423     11
30:      0      1      0 pc 11821062     11
26:      0      1      0 pc 7275972 11886598
27:      0      1  46432 pc 7275972  46432
26:      0      1      0 pc 9549068  46432
27:      0      1    181 pc 9549068    181
30:      0      1      0 pc 6142123    181
26:      0      1      0 pc 1372091 6142123
27:      0      1  23992 pc 1372091  23992
26:      0      1      0 pc 2355985  23992
27:      0      1     93 pc 2355985     93
30:      0      1      0 pc 6827258     93
26:      0      1      0 pc 6578112 6892794
27:      0      1  26924 pc 6578112  26924
26:      0      1      0 pc 4195236  26924
27:      0      1    105 pc 4195236    105
30:      0      1      0 pc 13811311    105
26:      0      1      0 pc 14195367 13876847
27:      0      1  54206 pc 14195367  54206
26:      0      1      0 pc 9001015  54206
27:      0      1    211 pc 9001015    211
30:      0      1      0 pc 13320494    211
*/
