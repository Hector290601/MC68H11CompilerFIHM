#-*- coding: utf-8 -*-

def get_instrucions_set():
    data = dict()
    file = open("../docs/op_codes_dictionarie.csv", "r")
    for instruction in file:
        instructions = instruction.split(",")
        data[instructions[0]] = instructions[1:-1]
    return data

if __name__ == "__main__":
    print(get_instrucions_set())
