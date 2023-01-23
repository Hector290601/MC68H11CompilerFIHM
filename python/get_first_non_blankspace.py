# -*- coding: utf-8 -*-

def get_first_non_blankspace(string):
    for i in range(len(string)):
        if string[i] != " ":
            return i

def get_first_blankspace(string):
    for i in range(len(string)):
        if string[i] == " ":
            return i

def find_parameters(string):
    position = 0
    last = position
    args = []
    line = string
    while position != None:
        position = get_first_non_blankspace(line)
        last = position
        line = line[position:]
        position = get_first_blankspace(line)
        arg = line[:position]
        args.append(arg)
        line = line[position:]
    return args

if __name__ == "__main__":
    value = input(": ")
    """
    position = get_first_non_blankspace(value)
    print("{}[{}]: {}".format(value, position, value[position]))
    value = value[position:]
    position = get_first_blankspace(value)
    print("{}[{}]: {}".format(value, position, value[position]))
    """
    print(find_parameters(value))
