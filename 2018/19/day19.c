// ip 2

#include <stdio.h>

int pc = 0;
long r0, r1, r3, r4, r5 = 0;
// r0 = r1 = r3 = r4 = r5 = 0;

void preg() {
  printf("ip=%d [%ld, %ld, %d, %ld, %ld, %ld]\n", pc, r0, r1, pc, r3, r4, r5);
}

void clock() {
switch(pc) {
case 0:	// addi 2 16 2
	pc = pc + 16;
	break;
case 1:	// seti 1 4 1
	r1 = 1;
	pc += 1;
case 2:	// seti 1 2 4
	r4 = 1;
	pc += 1;
case 3:	// mulr 1 4 3
	r3 = r1 * r4;
	pc += 1;
case 4:	// eqrr 3 5 3
	r3 = r3 == r5 ? 1 : 0;
	pc += 1;
case 5:	// addr 3 2 2
	pc += r3;
	break;
case 6:	// addi 2 1 2
	pc += 1;
	break;
case 7:	// addr 1 0 0
	r0 = r1 + r0;
	pc += 1;
case 8:	// addi 4 1 4
	r4 = r4 + 1;
	pc += 1;
case 9:	// gtrr 4 5 3
	r3 = r4 > r5 ? 1 : 0;
	pc += 1;
case 10:	// addr 2 3 2
	pc += r3;
	break;
case 11:	// seti 2 7 2
	pc = 2;
	break;
case 12:	// addi 1 1 1
	r1 += 1;
	pc += 1;
case 13:	// gtrr 1 5 3
	r3 = r1 > r5 ? 1 : 0;
	pc += 1;
case 14:	// addr 3 2 2
	pc = r3 + pc;
	break;
case 15:	// seti 1 0 2
	pc = 1;
	break;
case 16:	// mulr 2 2 2
	pc = pc * pc;
	break;
case 17:	// addi 5 2 5
	r5 += 2;
	pc += 1;
case 18:	// mulr 5 5 5
	r5 = r5 * r5;
	pc += 1;
case 19:	// mulr 2 5 5
	r5 = pc * r5;
	pc += 1;
case 20:	// muli 5 11 5
	r5 = r5 * 11;
	pc += 1;
case 21:	// addi 3 4 3
	r3 = r3 + 4;
	pc += 1;
case 22:	// mulr 3 2 3
	r3 = r3 * pc;
	pc += 1;
case 23:	// addi 3 7 3
	r3 = r3 + 7;
	pc += 1;
case 24:	// addr 5 3 5
	r5 = r5 + r3;
	pc += 1;
case 25:	// addr 2 0 2
	pc = pc + r0;
	break;
case 26:	// seti 0 1 2
	pc = 0;
	break;
case 27:	// setr 2 1 3
	r3 = pc;
	pc += 1;
case 28:	// mulr 3 2 3
	r3 = r3 * pc;
	pc += 1;
case 29:	// addr 2 3 3
	r3 = pc + r3;
	pc += 1;
case 30:	// mulr 2 3 3
	r3 = pc * r3;
	pc += 1;
case 31:	// muli 3 14 3
	r3 = r3 * 14;
	pc += 1;
case 32:	// mulr 3 2 3
	r3 = r3 * pc;
	pc += 1;
case 33:	// addr 5 3 5
	r5 = r5 + r3;
	pc += 1;
case 34:	// seti 0 9 0
	r0 = 0;
	pc += 1;
case 35:	// seti 0 8 2
	pc = 0;
	break;
}
    pc += 1;
}


int main(int argc, char *argv[]) {
  int part1 = 1;
  if (!part1) {
    r0 = 1;
  }
  long cycle = 0;
  while(pc < 37) {
    cycle += 1;
    if (part1) {
      preg();
    } else {
      if (cycle % 1000000 == 0) {
        printf("cycle: %ld ", cycle);
        preg();
      }
    }
    clock();
  }
  preg();
}
