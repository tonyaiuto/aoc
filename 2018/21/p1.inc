// int r0, r1, r2, r4, r5;
void prog() {
l0:	r4 = 123;                      // seti 123 0 4
l1:	r4 = r4 & 456;                 // bani 4 456 4
l2:	r4 = r4 == 72;                 // eqri 4 72 4
l3:	if (r4) goto l5;               // addr 4 3 3
	preg(4);
l4:	goto l1;                       // seti 0 0 3
l5:	r4 = 0;                        // seti 0 6 4
l6:	r5 = r4 | 65536;               // bori 4 65536 5
l7:	r4 = 1855046;                  // seti 1855046 9 4
l8:	r2 = r5 & 255;                 // bani 5 255 2
l9:	r4 = r4 + r2;                  // addr 4 2 4
l10:	r4 = r4 & 16777215;            // bani 4 16777215 4
l11:	r4 = r4 * 65899;               // muli 4 65899 4
l12:	r4 = r4 & 16777215;            // bani 4 16777215 4
l13:	r2 = 256 > r5;                 // gtir 256 5 2
l14:	if (r2) goto l16;              // addr 2 3 3
l15:	goto l17;                      // addi 3 1 3
l16:	goto l28;                      // seti 27 0 3
l17:	r2 = 0;                        // seti 0 9 2
l18:	r1 = r2 + 1;                   // addi 2 1 1
l19:	r1 = r1 * 256;                 // muli 1 256 1
l20:	r1 = r1 > r5;                  // gtrr 1 5 1
l21:	if (r1) goto l23;              // addr 1 3 3
l22:	goto l24;                      // addi 3 1 3
l23:	goto l26;                      // seti 25 5 3
l24:	r2 = r2 + 1;                   // addi 2 1 2
	preg(25);
l25:	goto l18;                      // seti 17 0 3
l26:	r5 = r2;                       // setr 2 7 5
	preg(27);
l27:	goto l8;                       // seti 7 9 3
l28:	r2 = r4 == r0;                 // eqrr 4 0 2
l29:	if (r2) goto l31;              // addr 2 3 3
	preg(30);
l30:	goto l6;                       // seti 5 3 3
l31:	return;
}
