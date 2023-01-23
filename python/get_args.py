# -*- coding: utf-8 -*-

def get_first_non_blankspace(string):
    for i in range(len(string)):
        if string[i] != " ":
            return i

def get_first_blankspace(string):
    for i in range(len(string)):
        if string[i] == " ":
            return i

def get_args(string):
    position = 0
    args = []
    line = string
    while position != None:
        if position < len(line):
            if line[position] == "*":
                return args
        position = get_first_non_blankspace(line)
        if position == None:
            return args
        if position < len(line):
            if line[position] == "*":
                return args
        line = line[position:]
        position = get_first_blankspace(line)
        arg = line[:position]
        args.append(arg)
        if position == None:
            return args
        if position < len(line):
            if line[position] == "*":
                return args
        line = line[position:]
    return args

if __name__ == "__main__":
    value = input(": ")
    print(get_args(value))
