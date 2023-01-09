* This program calculates the decimal value (in ASCII code) of
* an 8 bits unsigned binary number.

DATA	EQU	$0000	RAM
PROGRAM	EQU	$C000	ROM
RESET	EQU	$FFFE	RESET VECTOR

	ORG	DATA
INPUT	RMB	1	input is an 8 bits unsigned binary number
OUTPUT	RMB	3	output is an ASCII coded decimal value

	ORG	PROGRAM
START	LDAA	INPUT	get input data in accumulator A
	LDX	#OUTPUT	let index register X point to most significant digit of result
	LDAB	#'0'	initialise accumulator B to ASCII code for zero
SF100	SUBA	#100	subtract 100 from input data
	BCS	NO100	if there was a borrow there was less than 100 to start with
	INCB		if there was no borrow we found one 100
	BRA	SF100	search for another 100
NO100	STAB	0,X	write result to memory
	ADDA	#100	correct input data
	LDAB	#'0'	initialise accumulator B to ASCII code for zero
SF10	SUBA	#10	subtract 10 from input data
	BCS	NO10	if there was a borrow there was less than 10 to start with
	INCB		if there was no borrow we found one 10
	BRA	SF10	search for another 10
NO10	STAB	1,X	write result to memory
	ADDA	#10	correct input data
	ADDA	#'0'	add ASCII code for zero to data left (should be less than 10)
	STAA	2,X	write least significant digit to memory
LOOP	BRA	LOOP	nice way to stop without running wild

	ORG	RESET
	FDB	START	initialise reset vector