# -*- coding: utf-8 -*-
from data.type_values import Number, PowNumber

#функция для вычисления выражений с числами
def calculate(values, types_of_elements):
    values = [Number(int(elem)) if (type(elem) == str and elem.isdigit()) else elem for elem in values]
    #пока есть в выражении скобка, нужно выполнять в ней первым делом операции
    while '(' in values:
        right_braket_index = values.index(")")
        left_braket_index = 0
        while values[left_braket_index+1:right_braket_index].count('(') != 0:
            left_braket_index = values.index("(", left_braket_index+1, right_braket_index)
        #здесь будет происходить рекурсия
        value, type_value = calculate(values[left_braket_index+1:right_braket_index], types_of_elements[left_braket_index+1:right_braket_index])
        del values[left_braket_index: right_braket_index+1]; del types_of_elements[left_braket_index: right_braket_index+1]
        values.insert(left_braket_index, value[0]); types_of_elements.insert(left_braket_index, type_value[0])
    #пока есть знак возведения в степень числа
    while "pow" in types_of_elements:
        indeks = values.index("^");result = values[indeks - 1] ** values[indeks + 1];
        del values[indeks - 1: indeks + 2]; del types_of_elements[indeks - 1: indeks + 2]
        values.insert(indeks-1, result); types_of_elements.insert(indeks-1, result.getType())
    #пока есть знак умножения
    while "mull" in types_of_elements:
        indeks = values.index("*"); result = values[indeks - 1] * values[indeks + 1]
        del values[indeks - 1: indeks + 2]; del types_of_elements[indeks - 1: indeks + 2]
        values.insert(indeks-1, result); types_of_elements.insert(indeks-1, result.getType())
    #пока есть знак деления
    while "div" in types_of_elements:
        indeks = values.index("/"); result = values[indeks - 1] / values[indeks + 1]
        if result()[-1] == 0: print(f"Ошибка в ходе выполнения операции деления {str(values[indeks - 1])} на {str(values[indeks + 1])}. Причина: НА НОЛЬ ДЕЛИТЬ НЕЛЬЗЯ")
        del values[indeks - 1: indeks + 2]; del types_of_elements[indeks - 1: indeks + 2]
        values.insert(indeks-1, result); types_of_elements.insert(indeks-1, result.getType())
    #пока есть знак сложения
    while "add" in types_of_elements:
        indeks = values.index("+"); result = values[indeks - 1] + values[indeks + 1]
        del values[indeks - 1: indeks + 2]; del types_of_elements[indeks - 1: indeks + 2]
        values.insert(indeks-1, result); types_of_elements.insert(indeks-1, result.getType())
    #пока есть знак вычитания
    while "sub" in types_of_elements:
        indeks = values.index("-"); result = values[indeks - 1] - values[indeks + 1]
        del values[indeks - 1: indeks + 2]; del types_of_elements[indeks - 1: indeks + 2]
        values.insert(indeks-1, result); types_of_elements.insert(indeks-1, result.getType())

    #возвращаем результат вычисления
    return values, types_of_elements

def get_result(values, types_of_elements, format="decimal"):
    if format == "decimal": return eval(''.join(elem for elem in values).replace("^", "**"))
    value, type_element = calculate(values, types_of_elements)
    return value[0](), type_element[0]
        