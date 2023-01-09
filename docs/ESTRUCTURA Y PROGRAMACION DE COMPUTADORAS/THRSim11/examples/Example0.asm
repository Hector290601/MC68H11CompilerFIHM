* This is a very simple program that adds the contents of address
* $0000 to the contents of address $0001 and stores the resulting
* sum in the memory location at address $0002. If there is an 
* overflow the contents of address $0003 is set to $FF else 
* address $0003 is cleared.

	ORG	$0000	start of RAM (data)
OPER1	RMB	1	reserve 1 memory byte for operand 1
OPER2	RMB	1	reserve 1 memory byte for operand 2
SUM	RMB	1	reserve 1 memory byte for sum
OVERFL	RMB	1	reserve 1 memory byte for overflow signal

FALSE	EQU	$00	equate constant FALSE to $00

	ORG	$C000	start of ROM (program)
START	LDAB	#FALSE	be optimistic (assume no overflow occurs)
	LDAA	OPER1	load operand 1 in accumulator A
	ADDA	OPER2	add operand 2 to accumulator A
	BVC	NOV	branch if no overflow occurs
	COMB		oops overflow: invert accumulator B
NOV	STAA	SUM	store result of addition
	STAB	OVERFL	store overflow signal
LOOP	BRA	LOOP	nice way to stop without running wild

	ORG	$FFFE	reset vector
	FDB	START	set to start of program