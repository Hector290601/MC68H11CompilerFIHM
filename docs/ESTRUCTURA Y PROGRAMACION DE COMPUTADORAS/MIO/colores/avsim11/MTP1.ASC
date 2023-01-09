*********************************************
*           Habilitacion de Registros
*********************************************
PORTA    EQU   $1000
PORTE    EQU   $100A
PACTL    EQU   $1026
ALMS     EQU   $0000
ALMV     EQU   $0001
ALMP     EQU   $0002
DOCE     EQU   $0003
********************************************
*           Configuracion de registros
********************************************
         ORG   $F800
         LDAA  #$80         *A=80
         STAA  PACTL        *$1026=80 dir. los datos en el pto. A

         LDAB  #$10         *DATO EN PTO. A
         STAB  PORTA

         LDAA  #$10         *BIT I DE CCR="1"
         TAP
         LDAA  #$04         *DOY PRIORIDAD
         STAA  $103C
         LDAA  #$F8         *VECT. DE INT.
         STAA  $FFD6
         LDAA  #$CE
         STAA  $FFD7

         LDAA  #$03         *QUE PINES SON TRANSMISION
         STAA  $1008        *Y CUALES RECEPCION
         LDAA  #$00         *LONGITUD
         STAA  $102C
         LDAA  #$33         *VELOCIDAD
         STAA  $102B
         LDAA  #$3C         *HAB. TRANS, RECEPC, E INTER.
         STAA  $102D
********************************************
*           Programa Principal
********************************************
DELINIC  LDAB  #$0C
         STAB  DOCE
DEL      LDAB  PORTA
         ANDB  #$0F
         CMPB  #$80
         BNE   PPS1
         LDAB  #$10
         JSR   TIMER   *AL MOTOR
         STAB  PORTA
         DEC   DOCE
         BEQ   REVINIC
PPS1     LSLB
         JSR   TIMER    *AL MOTOR
         STAB  PORTA
         DEC   DOCE
         BEQ   REVINIC
         JMP   DEL
REVINIC  LDAB  #$0C
         STAB  DOCE
REV      LDAB  PORTA
         ANDB  #$F0
         CMPB  #$10
         BNE   PPS2
         LDAB  #$80
         JSR   TIMER    *AL MOTOR
         STAB  PORTA
         DEC   DOCE
         BEQ   DELINIC
PPS2     LSRB
         JSR   TIMER
         STAB  PORTA
         DEC   DOCE
         BEQ   DELINIC
         JMP   REV

******** Timer
TIMER    LDAA  #$07
LOOP6    DECA
         BNE   LOOP6
         RTS
*******************************
*        FIN DEL P.P.  $F800
*******************************


*******************************************
*        Rutina de Servicio
*******************************************
         LDAA  #$00         *BIT I DE CCR='0'
         TAP
         LDAA  #$0C
         STAA  $102D

LOOP7    LDAA  $102E        *CHECA REG. DE ESTATUS PARA TRANS.
         ANDA  #$20
         BEQ   LOOP7

         LDAA  #$00         *DESHAB. TRANS, RECEP, E INTE.
         STAA  $102D

         LDAA  $102F        *EL DATO SE ALMACENA EN "A"
         ANDA  #$0F
         CMPA  #$0C         *SI A=0C ENTONCES VE A COMP
         BEQ   COMP
         CMPA  #$0D         *SI A=0D ENTONCES VE A TECLADO
         BEQ   TECLADO

******** COMP
COMP     LDAA  #$0C         *HAB. TRANS Y RECEP.
         STAA  $102D

LOOP8    LDAA  $102E        *CHECA REG. DE ESTATUS PARA TRANS
         ANDA  #$20
         BEQ   LOOP8

         LDAA  $102F        *EL DATO TRANS. EN A
         ANDA  #$0F
         CMPA  #$0F
         BEQ   ALMSC
         CMPA  #$0E
         BEQ   ALMSC
         JMP   LOOP8
ALMSC    STAA  ALMS

LOOP9    LDAA  $102E        *CHECA REG. DE ESTATUS PARA TRANS.
         ANDA  #$20
         BEQ   LOOP9

         LDAA  $102F        *EL DATO TRANS. EN A
         ANDA  #$0F
         CMPA  #$05
         BGE   ALMVC
         JMP   LOOP9
ALMVC    STAA  ALMV

LOOP10   LDAA  $102E        *CHECA REG. DE ESTATUS PARA TRANS.
         ANDA  #$20
         BEQ   LOOP10

         LDAA  #$00         *DESHAB. TRANS. Y RECEP.
         STAA  $102D

         LDAA  $102F
         ANDA  #$0F
         CMPA  #$01
         BGE   ALMPC
         JMP   LOOP10
ALMPC    STAA  ALMP
         JMP   PROCESA

******** TECLADO
TECLADO  LDAA  PORTE
         ANDA  #$0F
         CMPA  #$0F
         BEQ   ALMST
         CMPA  #$0E
         BEQ   ALMST
         JMP   TECLADO
ALMST    STAA  ALMS

LOOP11   LDAA  PORTE
         ANDA  #$0F
         CMPA  #$05
         BGE   ALMVT
         JMP   LOOP11
ALMVT    STAA  ALMV

LOOP12   LDAA  PORTE
         ANDA  #$0F
         CMPA  #$01
         BGE   ALMPT
         JMP   LOOP12
ALMPT    STAA  ALMP

*********PROCESA
PROCESA  LDAB  ALMS
         CMPB  #$0F
         BEQ   DELI
REVI     LDAB  PORTA
         ANDB  #$F0
         CMPB  #$80
         BNE   SI1
         LDAB  #$10
         JSR   TIMERI   *AL MOTOR
         STAB  PORTA
         DEC   ALMP
         BEQ   RDI
SI1      LSLB
         JSR   TIMERI   *AL MOTOR
         STAB  PORTA
         DEC   ALMP
         BEQ   RDI
         JMP   REVI
DELI     LDAB  PORTA
         ANDB  #$F0
         CMPB  #$10
         BNE   SI2
         LDAB  #$80
         JSR   TIMERI   *AL MOTOR
         STAB  PORTA
         DEC   ALMP
         BEQ   RDI
SI2      LSRB
         JSR   TIMERI   *AL MOTOR
         STAB  PORTA
         DEC   ALMP
         BEQ   RDI
         JMP   DELI

******** TIMERI
TIMERI   LDAA  ALMV
LOOPI6   DECA
         BNE   LOOPI6
         RTS

RDI      LDAA  #$10         *DESHABILITA INTERRUPCION
         TAP
         LDAA  #$3C         *HAB. TRANS, RECEP, E INT.
         STAA  $102D
         RTI
****************************************
*        FIN DE LA RUT DE SERV
****************************************