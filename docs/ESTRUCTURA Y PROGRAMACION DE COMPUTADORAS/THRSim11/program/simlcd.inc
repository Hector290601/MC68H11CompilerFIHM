* Include file for THRSim11 I/O box LCD Display
* Harry Broeders February 2000

* This file contains 5 subroutines and must be included *after* 
* your own code.
* - SETPOS	Set the current cursor position.
* - GETPOS	Get the current cursor position.
* - PUTC	Print a character at the current cursor position.
* - PUTS	Print a string at the current cursor position.
* - CLRSCR	Clear the screen and set the cursor to postion 0,0

LCDDATA	EQU	$1040
LCDCTRL	EQU	$1041

NEWLINE	EQU	$0D	New line character.

*PUTC	Print a character at the current cursor position.
* 	Input:	Register A should contain the character.
*	Output:	None.
*	Uses:	Register CCR is changed.

PUTC	STAA	LCDDATA
	RTS

*PUTS	Print a string at the current cursor position.
* 	Input:	Register X should contain the address of the string.
*		A null character ($00) must follow the string to
*		mark the end.
*	Output:	None.
*	Uses:	Register CCR is changed.

PUTS	PSHA
	PSHX
LPUTS	LDAA	0,X
	BEQ	ENDPUTS
	STAA	LCDDATA
	INX
	BRA	LPUTS
ENDPUTS	PULX
	PULA
	RTS

*CLRSCR	Clear the screen and set the cursor to postion 0,0
* 	Input:	None.
*	Output:	None.
*	Uses:	Register CCR is changed.

CLRSCR	CLR	LCDDATA
	RTS

*GETPOS	Get the current cursor position.
* 	Input:	None.
*	Output:	Register A contains the x position (0 to 19).
*		Register B contains the y position (0 to 3).
*	Uses:	Registers A, B, and CCR are changed.

GETPOS	LDAA	#5
	STAA	LCDDATA
	CLRA	
	LDAB	LCDCTRL
	PSHX
	LDX	#20
	IDIV
	PSHB
	XGDX
	PULA
	PULX
	RTS

*SETPOS	Set the current cursor position.
* 	Input:	Register A contains the x position (0 to 19).
*		Register B contains the y position (0 to 3).
*	Output:	None.
*	Uses:	Regsister CCR is changed.

SETPOS	PSHB
	PSHA
	LDAA	#20
	MUL
	PULA
	PSHA
	ABA
	STAA	LCDCTRL
	LDAA	#6		
	STAA	LCDDATA
	PULA
	PULB
	RTS
	