#-*- coding: utf-8 -*-
from get_instrucions_set import *
from get_direction_type import *
from file_selector import *

variables = []
start = 0
def compile_args(data, instruction):
    global start, variables
    if "ORG $" in instruction:
        try:
            start = instruction[instruction.index("$") + 1: instruction[instruction.index("$")].index(" ")]
        except:
            start = instruction[instruction.index("$") + 1:]
        start.replace("\n", "")
        start = int(start)
        return "<" + str(start) + ">\n"
    elif "END $" in instruction:
        try:
            start = instruction[instruction.index("$") + 1: instruction[instruction.index("$")].index(" ")]
        except:
            start = instruction[instruction.index("$") + 1:]
        start.replace("\n", "")
        start = int(start)
        return "<" + str(start) + ">\n 1"
    elif " EQU " in instruction:
        instruction = instruction.replace("\t", "")
        instruction = instruction.replace("\n", "")
        instruction = instruction.replace("  ", "")
        variables.append([instruction[:instruction.index(" ")], instruction[::-1][:instruction.index(" ") - 1]])
        return ""
    direction_type, valid, precompiled = get_direction_type(data, instruction)
    if type(direction_type) == type(0) and direction_type != 7:
        if precompiled.split(":")[-1].split(",")[0] == "N/A" and direction_type != 5:
            return "\n"
        size = precompiled.split(":")[-1].split(",")[0]
        if size != "N/A":
            start = start + int(size)
        print(direction_type)
        if direction_type == 8:
            print("Error 004 @ {}".format(instruction))
            return "Error 004 @ " + instruction
        args = precompiled.split(",")
        args = args[1:]
        if direction_type == 5 and len(args) == 0:
            return "<" + str(start) + ">:" + precompiled.split(":")[0] + "\n"
        final_args = ""
        for arg in args:
            if arg[:2] == "#$":
                arg = int(str(arg[2:]), 16)
                if len("{0:b}".format(arg)) < 16:
                    final_args = final_args + str(arg)
                else:
                    print("Error 007 @ {}".format(instruction))
                    return "Error 007 @ " + instruction
            elif arg[:2] == "#'":
                for letter in arg[:2]:
                    final_args = final_args + str(ord(letter))
            elif arg[:1] == "#":
                arg = int(str(arg[1:]), 16)
                if len("{0:b}".format(arg)) < 16:
                    final_args = final_args + str(arg)
                else:
                    print("Error 007 @ {}".format(instruction))
                    return "Error 007 @ " + instruction
            else:
                try:
                    arg = int(str(arg[5:]), 16)
                    if len("{0:b}".format(arg)) < 16:
                        final_args = final_args + str(arg)
                    else:
                        print("Error 007 @ {}".format(instruction))
                        return "Error 007 @ " + instruction
                except:
                    pass
            for variable in variables:
                if variable[0] == arg:
                    final_args = final_args + str(variable[1])
        compiled = "<" + str(start) + ">:" + precompiled.split(":")[0] + " " + final_args  + "\n"
        return compiled
    return ""

def main():
    data = get_instrucions_set()
    path = select_file()
    code = open(path, 'r')
    lines = code.readlines()
    out = path[:-4] + ".lst"
    out = open(out, 'w')
    end = False
    for line in lines:
        print(line.replace("\n", ""), end = ":")
        compiled = compile_args(data, line)
        if "\n 1" in compiled:
            end = True
            out.write(compiled[:compiled.index("\n 1")] + "\n")
            print(out.write(compiled[:compiled.index("\n 1")] + "\n"), end = '')
            break
        else:
            out.write(compiled)
            print(compiled, end='')
    if not end:
        out.write("Error 010 @ {}".format(lines[-1]))
        print("Error 010 @ {}".format(lines[-1]))

if __name__ == "__main__":
    main()
