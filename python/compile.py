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
    elif " EQU " in instruction:
        instruction = instruction.replace("\t", "")
        instruction = instruction.replace("\n", "")
        instruction = instruction.replace("  ", "")
        variables.append([instruction[:instruction.index(" ")], instruction[::-1][:instruction.index(" ") - 1]])
        return ""
    try:
        direction_type, valid, precompiled = get_direction_type(data, instruction)
    except:
        return ""
    if type(direction_type) == type(0) and direction_type != 7:
        if precompiled.split(":")[-1].split(",")[0] != "N/A":
            start = start + int(precompiled.split(":")[-1].split(",")[0])
        if direction_type == 8:
            return "Error @ " + instruction
        args = precompiled.split(",")
        args = args[1:]
        final_args = ""
        for arg in args:
            if arg[:2] == "#$":
                final_args = final_args + arg[2:]
            elif arg[:2] == "#'":
                for letter in arg[:2]:
                    final_args = final_args + str(ord(letter))
            for variable in variables:
                if variable[0] == arg:
                    final_args = final_args + str(variable[1])
        compiled = "<" + str(start) + ">:" + precompiled.split(":")[0] + " " + precompiled + "\n"
        return compiled
    return ""

def main():
    data = get_instrucions_set()
    path = select_file()
    code = open(path, 'r')
    lines = code.readlines()
    out = path[:-4] + ".lst"
    out = open(out, 'w')
    for line in lines:
        out.write(compile_args(data, line))

if __name__ == "__main__":
    main()
