#-*- coding:utf-8 -*-
import time
import os
from get_instrucions_set import *

"""
Return the direction type used on the function as an integrer from 0 to 5 and a args array to validate the directiionment type and an array adverting about some erros.
    +-------------+------------+
    |  Direction  |  Integrer  |
    |    type     |  asocied   |
    +-------------+------------+
    |     IMM     |      0     |
    +-------------+------------+
    |     DIR     |      1     |
    +-------------+------------+
    |     IDX     |      2     |
    +-------------+------------+
    |     IDY     |      3     |
    +-------------+------------+
    |     EXT     |      4     |
    +-------------+------------+
    |     INH     |      5     |
    +-------------+------------+
    |     REL     |      6     |
    +-------------+------------+
    |   COMMENT   |      7     |
    +-------------+------------+
    |    ERROR    |      8     |
    +-------------+------------+

"""
# get_direction_type {{{ 1
def get_direction_type(instruction_set, args = ""):
    #debug purposes only
    print(args, end=": ")
    # remueve espacios en blanco {{{2
    args = args.replace("  ", "")
    args = args.replace("  ", "")
    # }}}
    # remueve comentarios {{{2
    if "*" in args:
        depreciable = args.index("*")
        args = args[:depreciable]
        if len(args) == 0:
            return 7
    # }}}
    # formateo de cadenas {{{2
    # separa los argumentos por espacios
    args = args.split(" ")
    # selecciona el argumento que indica la orden
    instruction = args[0].lower()
    # }}}
    # Instruccion inexistente {{{2
    if instruction not in instruction_set:
        return 8, 1
    # }}}
    # Separa las tablas de equivalencias por tipo de direccionamiento {{{2
    data = instruction_set[instruction]
    supported_types = {
            "IMM": data[0],
            "DIR": data[2],
            "IDX": data[4],
            "IDY": data[6],
            "EXT": data[8],
            "INH": data[10],
            "REL": data[12]
            }
    # }}}
    i = 0
    for arg in args:
        if arg == " " or arg == "":
            args.pop(i)
        i = i + 1
    i = 0
    for arg in args:
        if arg == " " or arg == "":
            args.pop(i)
        i = i + 1
    # Comentario {{{2
    if len(args) == 0:
        return 7
    # }}}
    # Inmediato {{{2
    if supported_types["IMM"] != "":
        if len(args) == 2:
            arg = args[-1]
            if not "," in arg:
                if "#" in arg:
                    if "$" in arg:
                        arg = arg[2:]
                    else:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 16:
                            returnable = instruction_set[instruction][0] + "," + args[-1]
                            return 0, 0, returnable
                        else:
                            return 0, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return 0, 0
                    return 0, 1
    # }}}
    # Directo {{{2
    if supported_types["DIR"] != "":
        if len(args) == 2:
            arg = args[-1]
            if not "," in arg:
                if "#" not in arg:
                    if "$" in arg:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 8:
                            return instruction_set[instruction][4], 1, 0
                        else:
                            return instruction_set[instruction][4], 1, 1
                    except:
                        pass
                    if len(arg) <= 2:
                        return instruction_set[instruction][4], 1, 0
    # }}}
    # Extendido {{{2
    if supported_types["EXT"] != "":
        print(instruction_set[instruction][4], end="")
        if len(args) == 2:
            arg = args[-1]
            if not "," in arg:
                if "#" not in arg:
                    if "$" in arg:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 16:
                            return instruction_set[instruction][4], 4, 0
                        else:
                            return instruction_set[instruction][4], 4, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return instruction_set[instruction][4], 4, 0
                    return instruction_set[instruction][4], 4, 1
    # }}}
    # Indexado respecto a X {{{2
    if supported_types["IDX"] != "":
        if len(args) == 2:
            arg = args[-1]
            if ",X" in arg:
                arg = arg[:-2]
                if "#" not in arg:
                    if "$" in arg:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 8:
                            return instruction_set[instruction][6], 2, 0
                        else:
                            return instruction_set[instruction][6], 2, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return instruction_set[instruction][6], 2, 0
                    return instruction_set[instruction][6], 2, 1
    # }}}
    # Indexado respecto a Y {{{2
    if supported_types["IDY"] != "":
        if len(args) == 2:
            arg = args[-1]
            if ",Y" in arg:
                arg = arg[:-2]
                if "#" not in arg:
                    if "$" in arg:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 8:
                            return instruction_set[instruction][8],3,0
                        else:
                            return instruction_set[instruction][8],3,1
                    except:
                        pass
                    if len(arg) <= 4:
                        return instruction_set[instruction][8],3,0
                    return instruction_set[instruction][8],3,1
    # }}}
    # Inherente {{{2
    if supported_types["INH"] != "":
        if len(args) == 1:
            return instruction_set[instruction][10],5, 0
        else:
            return instruction_set[instruction][10],5, 0
    # }}}
    # Relativo {{{2
    if supported_types["REL"] != "":
        if len(args) > 1 and not args[-1].isnumeric():
            return instruction_set[instruction][12],6, 0
        else:
            return instruction_set[instruction][12],6, 1

# }}}
# }}}

if __name__ == "__main__":
    # Tests {{{ 1
    data = get_instrucions_set()
    # Inmediato {{{ 2
    print("IMM:")
    print(get_direction_type(data, "ldaa #$45   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB #11   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAA #'k   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD #$1789  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX #1531   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA #$7C   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA #$F0   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY #$ABCD  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY #$ABCDE * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABCD   * ESTO ES UN COMENTARIO"))
    # }}}
    # Directo {{{ 2
    print("DIR:")
    print(get_direction_type(data, "ldaa $45    * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 11     * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $17     * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 15      * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7C    * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0    * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $AB     * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABCDE  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY #$AB    * ESTO ES UN COMENTARIO"))
    # }}}
    # Extendido {{{ 2
    print("EXT:")
    print(get_direction_type(data, "ldaa $457C  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 1531    * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $1789   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 65000   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABCD   * ESTO ES UN COMENTARIO"))
    # }}}
    # Indexado X {{{ 2
    print("IDX:")
    print(get_direction_type(data, "ldaa $457C,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 151,X  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $255,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 60,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABC,X  * ESTO ES UN COMENTARIO"))
    # }}}
    # Indexado Y {{{ 2
    print("IDY:")
    print(get_direction_type(data, "ldaa $457C,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 151,Y  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $255,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 60,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABC,Y  * ESTO ES UN COMENTARIO"))
    # }}}
    # Inherente {{{ 2
    print("INH:")
    print(get_direction_type(data, "NOP         * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "inx         * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "DEX         * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data , "INY        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "DEY         * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "MUL         * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "XGDX        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "XGDY        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "NEGA        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "NEGB        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "NEGE        * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "NEGB 12     * ESTO ES UN COMENTARIO"))
    # }}}
    # Relativo {{{ 2
    print("REL:")
    print(get_direction_type(data, "BNE INICIO * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BCC FIN * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BCS FIN * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BEQ FIN * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BGE FIN * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BLE FIN * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "BMI FIN * ESTO ES UN COMENTARIO"))
    # }}}
    # Comentario {{{ 2
    print("COMENTARIO: ")
    print(get_direction_type(data, "* ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "* NOP"))
    # }}}
    # }}}
