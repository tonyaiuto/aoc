
#include <stdio.h>

long r0, r4, r5;

void preg(int l) {
  printf("%2d: %6ld %6lx %6lx\n", l, r0, r4, r5);
}


int prog() {
#if 0
  while (1) {
    r4 = 123;                      // seti 123 0 4
    r4 = r4 & 456;                 // bani 4 456 4
    r4 = r4 == 72;                 // eqri 4 72 4
    if (r4) break;
    preg(4);
    return -1;
  }
#endif

  long i_count = 0;
  long loop_start = 0;
  r4 = 0;                        // seti 0 6 4
  while(1) {
    // preg(2);
    r5 = r4 | 0x10000;               // bori 4 65536 5
    r4 = 1855046;                  // seti 1855046 9 4
    // hex(1855046) = '0x1c4e46'
    i_count += 2;

    while(1) {
      r4 = r4 + (r5 & 0xff);
      // clip to 24 bits
      r4 = r4 & 0xffffff;            // bani 4 16777215 4
      r4 = r4 * 65899;               // muli 4 65899 4
      r4 = r4 & 0xffffff;            // bani 4 16777215 4
      i_count += 5;

      if (256 > r5)  {
        break;
      } 
      r5 = r5 / 256;
      i_count += r5;
    }
    // assert r5 < 256 && r4 <= 0xffffff

    if (r4 == 0x16c5e5 && r5 == 1) {
      if (loop_start > 0) {
        printf("loop period=%ld for r0=%ld\n", i_count - loop_start, r0);
        break;
      }
      loop_start = i_count;
    }
    if (r4 == r0) {
      printf("done: i_count=%ld for r0=%ld\n", i_count, r0);
      break;              // addr 2 3 3
    }
  }
  return 0;
}

int main(int argc, char *argv[]) {
  // r0 = 9079325;
  // r0 = 0xffffff;
  for (r0 = 0; r0 <= 0xffffff; r0++) {
    prog();
  }
}
