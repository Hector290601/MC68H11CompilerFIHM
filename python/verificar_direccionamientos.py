#-*- coding:utf-8 -*-

from get_direction_type import *
from file_selector import *
from get_instrucions_set import *

def main():
    data = get_instrucions_set()
    path = select_file()
    code = open(path, 'r')
    lines = code.readlines()
    for line in lines:
        print(get_direction_type(data, line))

if __name__ == "__main__":
    main()
