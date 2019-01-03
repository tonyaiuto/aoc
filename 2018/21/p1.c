
#include <stdio.h>

int r0, r1, r2, r4, r5;

void preg(int l) {
  printf("%2d: %6d %6d %6d pc %6d %6d\n", l, r0, r1, r2, r4, r5);
}

#include "p1.inc"

int main(int argc, char *argv[]) {
  r0 = r1 = r2 = r4 = r5 = 0;
  prog();
}
