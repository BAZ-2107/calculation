# -*- coding: utf-8 -*-

#импортируем необходимые библиотеки

#os - для возможности смен директорий(для чтения файлов из различных директорий)
import os

#sys - для поддержки корректной работы приложения
import sys

"""из директории data импортируем файлы decode, design, calculation"""
from data import decode, design, calculation


def main(string):
    values, types_of_elements = read_to_values(string)
    if not any(elem in values for elem in ["=", ">", "<", "≥", "≤"]):
        return calculation.get_result(values, types_of_elements, format="ЧЧФ")
    #print(values, types_of_elements)



#Запуск программы
if __name__ == "__main__":
    #переходим в директорию files для считывания всех файлов оттуда
    os.chdir("files")
    #запускаем обработчик событий
    app = design.QApplication(sys.argv)
    #создаем объект главного окна приложения
    window = design.MainWindow()
    #запускаем window
    window.show()
    #запускаем обработчик, отлавливающий ошибки
    sys.excepthook = design.except_hook
    #завершаем корректно программу
    sys.exit(app.exec())
    """
    string = '4^(3/2)*((2-1)/8)'
    print(main(string))"""