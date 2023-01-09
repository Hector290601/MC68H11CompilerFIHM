* This program calculates the decimal value (in ASCII code) of
* an 8 bits unsigned binary number present at external pins PC7 to PC0.
* The result will be displayed on the LCD display of the I/O box.
* Each conversion is triggered by a rising edge of the Strobe A pin.
* The program uses the IRQ interrupt.

STACK	EQU	$00FF	Bottom of Stack
PROGRAM	EQU	$C000	ROM
LCDDATA	EQU	$1040	LCD display
IRQ	EQU	$FFF2	IRQ vector
RESET	EQU	$FFFE	RESET vector

PIOC	EQU	$1002	Parallel I/O Control Register
PORTCL	EQU	$1005	Alternate Latched Port C
DDRC	EQU	$1007	Data Direction for port C

	ORG	PROGRAM
* main program
START	LDS	#STACK	initialise stack
	CLR	DDRC	initialise port C to all inputs
	LDAA	#%01000010
	STAA	PIOC	enable Strobe A interrupt on rising edge
	CLI		enable IRQ
LOOP	BRA	LOOP	wait for IRQ or RESET
		
* IRQ interrupt service routine
IRQISR	LDAA	PIOC
	BPL	ERROR	IRQ generated but not by Strobe A pin
	CLRA	
	STAA	LCDDATA	clear LCD display	
	LDAA	PORTCL	get input data in accumulator A
	LDAB	#'0'	initialise accumulator B to ASCII code for zero
SF100	SUBA	#100	subtract 100 from input data
	BCS	NO100	if there was a borrow there was less than 100 to start with
	INCB		if there was no borrow we found one 100
	BRA	SF100	search for another 100
NO100	STAB	LCDDATA	display result on LCD
	ADDA	#100	correct input data
	LDAB	#'0'	initialise accumulator B to ASCII code for zero
SF10	SUBA	#10	subtract 10 from input data
	BCS	NO10	if there was a borrow there was less than 10 to start with
	INCB		if there was no borrow we found one 10
	BRA	SF10	search for another 10
NO10	STAB	LCDDATA	display result on LCD
	ADDA	#10	correct input data
	ADDA	#'0'	add ASCII code for zero to data left (should be less than 10)
	STAA	LCDDATA	display least significant digit on LCD
	RTI		return from interrupt

* error routine
ERRSTR	FCC	"ERROR"
ERROR	CLRA	
	STAA	LCDDATA	clear LCD display
	LDAB	#5	number of characters in error message
	LDX	#ERRSTR 
MORE	LDAA	0,X	get character from error message
	STAA	LCDDATA	display it on LCD
	INX
	DECB		repeat until all characters are displayed
	BNE	MORE
	RTI

	ORG	RESET
	FDB	START	initialise reset vector
	ORG	IRQ
	FDB	IRQISR	initialise IRQ vector