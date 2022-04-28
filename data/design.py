# -*- coding: utf-8 -*-
import json
import sys
import os
from math import sqrt
#импортируем из библиотеки PyQt5 необходимые модули
from PyQt5.QtCore import *
from PyQt5.QtGui import *
"""импортируем из PyQt5.QtWidgets: QApplication - для обработки инициализации и завершения работы приложения
QMainWindow - класс отображения главного окна"""
from PyQt5.QtWidgets import *
"""импортируем uic, чтобы файл с дизайном в процессе разработки было легче считывать"""
from PyQt5 import uic


#класс для отображения главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #считываем файл с дизайном из директории design
        uic.loadUi("design_files\design.ui", self)
        self.calculation.triggered.connect(self.open_calculator)
    
    def open_calculator(self):
        self.calculator = Calculator(self)
        self.calculator.show()


"""РАЗДЕЛ КАЛЬКУЛЯТОРА"""
#Создается класс, наследованный от QValidator. Его задача - фильтр ввода символов с клавиатуры
class Valid(QValidator):
    #при инициализации объекта класса
    def __init__(self):
        super().__init__()
        #из текстового файла читаем в массив символы, которые можно будет вводить с клавиатуры
        with open("text_files\signs_in_calculator.txt") as file: self.massiv_allowed_symbols = [elem for elem in file.read().split()]
    
    #вот он, метод для фильтровки символов!
    def validate(self, string, pos):
        if string == "": return (2, string, pos)
        if string[pos-1] in self.massiv_allowed_symbols: return (2, string, pos)
        return (0, string, pos)


#класс для отображения окна калькулятора
class Calculator(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI()

    def initUI(self):
        #считываем файл с дизайном нашего окна
        uic.loadUi("design_files\calculator.ui", self)
        self.dict_replaced_symbols = {"^": "**", "√": "sqrt"}
        #при нажатии кнопки Вычислить вычисляется введенное выражение
        self.count.clicked.connect(self.calculation)
        #Добавляется фильтр ввода в поле ввода
        self.expression.setValidator(Valid())
        #Символ добавляется в поле ввода, при нажатии на кнопку с ним
        for elem in self.buttonGroup.buttons(): elem.clicked.connect(self.full)
    
    #метод добавления символа в поле ввода
    def full(self):
        indeks = self.expression.cursorPosition(); text = self.expression.text(); self.expression.setText(text[:indeks] + self.sender().text() + text[indeks:])
        
    #метод ддля вычисления выражения
    def calculation(self):
        expression = "".join(elem if elem not in self.dict_replaced_symbols.keys() else self.dict_replaced_symbols[elem] for elem in self.expression.text()).replace("mod", "%")
        try: self.show_result.setText(str(round(eval(expression), int(self.count_numbers.currentText()))))
        except ZeroDivisionError: self.show_result.setText("На ноль делить нельзя")
        except Exception: self.show_result.setText("Не удалось вычислить выражение")
"""КОНЕЦ РАЗДЕЛА КАЛЬКУЛЯТОР"""

#функция для отлавливания ошибок
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    os.chdir("..")
    app = QApplication(sys.argv)
    #создаем объект главного окна приложения
    window = MainWindow()
    #запускаем window
    window.show()
    #запускаем обработчик, отлавливающий ошибки
    sys.excepthook = except_hook
    #завершаем корректно программу
    sys.exit(app.exec())