#-*- coding: utf-8 -*-

from get_instrucions_set import *

def main():
    data = get_instrucions_set()
    instruction = input("Instruction: ")
    instruction = instruction.lower()
    if instruction in data:
        print(data[instruction])

if __name__ == "__main__":
    main()
