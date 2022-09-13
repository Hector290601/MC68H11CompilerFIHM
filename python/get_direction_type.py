#-*- coding:utf-8 -*-
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

def get_direction_type(instruction_set, args = ""):
    print(args, end=": ")
    args = args.replace("  ", "")
    args = args.replace("  ", "")
    if "*" in args:
        depreciable = args.index("*")
        args = args[:depreciable]
    args = args.split(" ")
    instruction = args[0].lower()
    if instruction not in instruction_set:
        return 8, 1
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
    if len(args) == 0:
        return 7
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
                            return 0, 0
                        else:
                            return 0, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return 0, 0
                    return 0, 1
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
                            return 1, 0
                        else:
                            arg = str(arg)
                    except:
                        pass
                    if len(arg) <= 2:
                        return 1, 0
    if supported_types["EXT"] != "":
        if len(args) == 2:
            arg = args[-1]
            if not "," in arg:
                if "#" not in arg:
                    if "$" in arg:
                        arg = arg[1:]
                    try:
                        arg = int(arg)
                        if arg < 2 ** 16:
                            return 4, 0
                        else:
                            return 4, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return 4, 0
                    return 4, 1
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
                            return 2, 0
                        else:
                            return 2, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return 2, 0
                    return 2, 1
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
                            return 3, 0
                        else:
                            return 3, 1
                    except:
                        pass
                    if len(arg) <= 4:
                        return 3, 0
                    return 3, 1
    if supported_types["INH"] != "":
        if len(args) == 1:
            return 5, 0
        else:
            return 5,1

if __name__ == "__main__":
    data = get_instrucions_set()
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
    print("EXT:")
    print(get_direction_type(data, "ldaa $457C  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 1531    * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $1789   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 65000   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB   * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABCD   * ESTO ES UN COMENTARIO"))
    print("IDX:")
    print(get_direction_type(data, "ldaa $457C,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 151,X  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $255,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 60,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1,X * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABC,X  * ESTO ES UN COMENTARIO"))
    print("IDY:")
    print(get_direction_type(data, "ldaa $457C,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDAB 151,Y  * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDD $255,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDX 60,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ADDA $7CB,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "ANDA $F0B1,Y * ESTO ES UN COMENTARIO"))
    print(get_direction_type(data, "LDY $ABC,Y  * ESTO ES UN COMENTARIO"))
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

