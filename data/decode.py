# -*- coding: utf-8 -*-
#импортируем json - для чтения файла "signs.json"
import json

def read_to_values(line):
    #считываем файл "signs.json" в переменную signs
    with open("signs.json") as x:
        signs = json.load(x)
    #создаем пустые массивы, в values хранится объект, в types_of_elements - тип объекта
    values = []; types_of_elements = []
    #циклически проходим по строке line, "разбивая" ее на объекты(числа, знаки, переменные)
    for index, elem in enumerate(line.replace(' ', '')):
        if elem.isdigit():
            if len(values) == 0 or types_of_elements[-1] != 'number':
                values.append(elem); types_of_elements.append('number');
            else:
                values[-1] += elem
        else:
            if elem.isalpha():
                values.append(elem); types_of_elements.append('letter');
            elif elem in signs:
                values.append(elem); types_of_elements.append(signs[elem]);
    #возвращаем массивы values и types_of_elements
    return values, types_of_elements

print(read_to_values("5(xав-5)"))