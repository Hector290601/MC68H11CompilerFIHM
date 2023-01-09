$ALLPUBLIC
;	Demo Program for 68HC11
;	Written by Ken Anderson
;	Dec 87
;
;	This program is intended to demonstrate features of
;	the 6811 CPU that are easily visualized on Avocet's
;	AVSIM11 Simulator.
;
;	The functions of this program include:
;
;	1. MAIN routine reads the bit pattern from PORT C
;	   and cycles it on the LEDs attached to PORT B
;	   (like a light chaser) where HI bits represent
;	   LIGHT ON (or vice-versa, of course).
;	   The light chaser rotates alternately to the right,
;	   then to the left at a rate corresponding to
;	   the binary value of PORT C's bit pattern.
;
;	2. Timer interrupt routine changes the rotation direction
;	   on each countdown.
;
;	3. SCI is driving a second task:
;	   On interrupt, read ASCII character in SCI's RDR, and buffer it.
;	   Special character <CR> clears the buffer contents - mostly for
;	   visual effect in the simulator!
;
;
;

; 	6811 Map
     SEG REGS
_STARTREGS
     SEG CODE

PORTA	EQU	_STARTREGS+00H	;I/O Port A
PIOC	EQU	_STARTREGS+02H	;Parallel I/O Control Register
PORTC	EQU	_STARTREGS+03H	;I/O Port C
PORTB	EQU	_STARTREGS+04H	;I/O Port B
PORTCL	EQU	_STARTREGS+05H	;Alternate Latched Port C
DDRC	EQU	_STARTREGS+07H	;Data Direction for Port C
PORTD	EQU	_STARTREGS+08H	;I/O Port D
DDRD	EQU	_STARTREGS+09H	;Data Direction for Port D
PORTE	EQU	_STARTREGS+0AH	;I/O Port E
CFORC	EQU	_STARTREGS+0BH	;Compare Force Register
OC1M	EQU	_STARTREGS+0CH	;OC1 Action Mask register
OC1D	EQU	_STARTREGS+0DH	;OC1 Action Data Register
TCNT	EQU	_STARTREGS+0EH	;Timer Counter Register
TIC1	EQU	_STARTREGS+10H	;Input Capture 1 Register
TIC2	EQU	_STARTREGS+12H	;Input Capture 2 Register
TIC3	EQU	_STARTREGS+14H	;Input Capture 3 Register
TOC1	EQU	_STARTREGS+16H	;Output Compare 1 Register
TOC2	EQU	_STARTREGS+18H	;Output Compare 2 Register
TOC3	EQU	_STARTREGS+1AH	;Output Compare 3 Register
TOC4	EQU	_STARTREGS+1CH	;Output Compare 4 Register
TOC5	EQU	_STARTREGS+1EH	;Output Compare 5 Register
TCTL1	EQU	_STARTREGS+20H	;Timer Control Register 1
TCTL2	EQU	_STARTREGS+21H	;Timer Control Register 2
TMSK1	EQU	_STARTREGS+22H	;Main Timer Interrupt Mask Register 1
TFLG1	EQU	_STARTREGS+23H	;Main Timer Interrupt Flag Register 1
TMSK2	EQU	_STARTREGS+24H	;Main Timer Interrupt Mask Register 2
TFLG2	EQU	_STARTREGS+25H	;Main Timer Interrupt Flag Register 2
PACTL	EQU	_STARTREGS+26H	;Pulse Accumulator Control Register
PACNT	EQU	_STARTREGS+27H	;Pulse Accumulator Count Register
SPCR	EQU	_STARTREGS+28H	;SPI Control Register
SPSR	EQU	_STARTREGS+29H	;SPI Status Register
SPDR	EQU	_STARTREGS+2AH	;SPI Data In/Out
BAUD	EQU	_STARTREGS+2BH	;SCI Baud Rate Control
SCCR1	EQU	_STARTREGS+2CH	;SCI Control Register 1
SCCR2	EQU	_STARTREGS+2DH	;SCI Control Register 2
SCSR	EQU	_STARTREGS+2EH	;SCI Status Register
SCDR	EQU	_STARTREGS+2FH	;SCI Data (Read RDR, Write TDR)
ADCTL	EQU	_STARTREGS+30H	;A-to-D Control Register
ADR1	EQU	_STARTREGS+31H	;A-to-D Result Register 1
ADR2	EQU	_STARTREGS+32H	;A-to-D Result Register 2
ADR3	EQU	_STARTREGS+33H	;A-to-D Result Register 3
ADR4	EQU	_STARTREGS+34H	;A-to-D Result Register 4
OPTION	EQU	_STARTREGS+39H	;System Configuration Options
COPRST	EQU	_STARTREGS+3AH	;Arm/Reset COP Timer Circuitry
PPROG	EQU	_STARTREGS+3BH	;EEPROM Programming Control Register
HPRIO	EQU	_STARTREGS+3CH	;Highest Priority I-Bit Interrupt & Misc.
INIT	EQU	_STARTREGS+3DH	;RAM and I/O Mapping Register
TEST1	EQU	_STARTREGS+3EH	;Factory TEST control register
CONFIG	EQU	_STARTREGS+3FH	;COP, ROM & EEPROM Enables

;	Constants

BUFSIZE	EQU	31		; Maximum Buffer size
RETURN	EQU	$0D		; Carriage Return

;	Variable Map

	DEFSEG	VARS,START=$0,ABSOLUTE
	SEG	VARS		; SC Mode RAM Starts at $0

PTRN	DS	1		; Pattern read from PORT 2
DIRN	DS	1		; Light chaser rotation direction
BUFPTR	DS	2		; Save X
BUFBASE	DS	BUFSIZE		; IRQ routine Buffer space

;	Stack

	DS	63
STACK	DS	1

	DEFSEG	MAINCODE,START=$E000	; Single Chip Mode ROM Starts at $E000
	SEG	MAINCODE	

MAIN:	LDAA	#%00000000	
	STAA	DDRC		; make port C input
	LDAA	#%00110000	; Baud 9600 & 8.0 MHz Xtal -> /13
	STAA	BAUD		; for SCI
	CLR	SCCR1		; 8-bit mode
	LDAA	#%00100100	; Receive circuit interrupts
	STAA	SCCR2		; for SCI
	LDAA	#%01000000	; Use Output Compare 2 Interrupt
	STAA	TMSK1		; of TIMER
	LDX	#0		; Init X points to buffer
	STX	BUFPTR
	LDS	#STACK		; Init stack
	CLI			; enable ints
	LDAA	PORTC		; get light chaser pattern
NEWPTRN:STAA 	PTRN		; save it to test switch setting changes
	STAA	PORTB		; set new pattern on lights
	BSR	SETOCR		; Setup OCR interrupt
	CLR	DIRN		; Start pattern to rotate rightwards
R1:	BSR	ROTATE		; show stack working
	CMPA	PTRN		; switches modified?
	BNE	NEWPTRN		; yes -> read them & start up
	BRA	R1		; no  -> just keep rotating

ROTATE:	LDAA	DIRN		; low bit of DIRN selects rotate direction
	RORA			; put direction bit into carry
	LDAA	PORTB		; get ready with data
	BCS	ROTLEFT		; HI = rotate left
	RORA			; put lo bit in carry
	ROR	PORTB		; rotates PORT B thru carry
	BRA	TSTPTRN		; end-of-loop test
ROTLEFT:ROLA			; put hi bit in carry
	ROL	PORTB		; rotates PORT B thru carry
TSTPTRN:LDAA	PORTC		; read switch bank
	RTS			


OCFIRQ:	INC	DIRN		; toggle lo-bit = rotate direction
	LDAA	#%01000000	; clear OC2F 
	STAA	TFLG1		; of TFLG1 
	BSR	SETOCR		; write OCR
	RTI			; wrap up software interrupt here too

SETOCR:	LDAA	PTRN		; Get input pattern, then
	LDAB	#$40		; use binary value * 40H for timer count
	MUL
	ADDD	TCNT		; Make relative to current count
	STD	TOC2		; Set Output Compare 2
	RTS

SCIRQ:	LDAA	SCSR		; To clear RDRF read SCSR then
	LDAA	SCDR		; Get char 
	LDX	BUFPTR
	CMPA	#$0D		; Special key - CR ?
	BNE	BUFCHAR		; no
CLEAR:	CLR	BUFBASE,X	; clear from BUFPTR to 0
	DEX			; above Buffer Base Address
	CPX	#0
	BPL	CLEAR
	BRA	SAVEPTR		; then reset buffer pointer
BUFCHAR:CPX	#BUFSIZE	; Any room left?
	BCC	EXIT		; No, if BUFPTR >= BUFSIZE
	STAA	BUFBASE,X	; save char
SAVEPTR:INX			; advance to next free position
	STX	BUFPTR
EXIT:	RTI			; done

;	Vectors are stored at top-of-memory

	DEFSEG	VCIRQ,START=$FFD6
	SEG	VCIRQ
	DW	SCIRQ		; SCI interrupt vector 

	DEFSEG	VOIRQ,START=$FFE6
	SEG	VOIRQ		; Leave others undefined -> AVSIM trap
	DW	OCFIRQ		; Output Compare 2 interrupt vector

	DEFSEG	VIRQ,START=$FFFE
	SEG	VIRQ
	DW	MAIN		; RESET vector
	
	END

