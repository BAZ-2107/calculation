# -*- coding: utf-8 -*-


def nod(a, b):                 # рекурсивная функция для нахождения наибольшего общего делителя для 2 целых чисел
    if b == 0: return a
    else: return nod(b, a % b)

class Integer:             # класс для хранения целого числа как объекта
    name = "Number"
    kind = "Integer"

    def __init__(self, number):
        self.number = number
        self.rational = (number, 1)
    
    def __str__(self):
        return str(self.number)
    
    def __add__(self, other):    # метод сложения
        a1,b1=self.rational; a2,b2=other.rational; a3,b3=a1*b2+b1*a2,b1*b2
        if a3 % b3 == 0: return Integer(a3 // b3)
        d = nod(a3, b3); return Rational(a3 // d, b3 // d)
    
    def __sub__(self, other):    # метод вычитания
        a1,b1=self.rational; a2,b2=other.rational; a3,b3=a1*b2-b1*a2,b1*b2
        if a3 % b3 == 0: return Integer(a3 // b3)
        d = nod(a3, b3); return Rational(a3 // d, b3 // d)

    def __mul__(self, other):   # метод умножения
        a1,b1=self.rational; a2,b2=other.rational; a3,b3=a1*a2,b1*b2
        if a3 % b3 == 0: return Integer(a3 // b3)
        d = nod(a3, b3); return Rational(a3 // d, b3 // d)
        
    def __truediv__(self, other):  # метод деления
        a1,b1=self.rational; a2,b2=other.rational; a3,b3=a1*b2,b1*a2
        if a2 == 0: return "На ноль делить нельзя"
        if a3 % b3 == 0: return Integer(a3 // b3)
        d = nod(a3, b3); return Rational(a3 // d, b3 // d)
    
    def __neg__(self):   # метод унарной операции минус
        return Integer(-1) * self
    
    def __pos__(self):   # метод унарной операции плюс
        return self    

class Rational(Integer):  # класс для хранения рационального числа как объекта(наследуется от класса Integer)
    kind = "Rational"

    def __init__(self, numerator, denominator):
        self.number = numerator, denominator
        self.rational = self.number

a = Rational(5, 10)
b = Integer(9)
operation = -a
print(operation)



#Объект - целое число, представленное в виде рациональной дроби
class Number:
    #число представляется в виде дроби. На вход - числитель и знаменатель
    def __init__(self, numerator=1, denominator=1):
        div = self.nod(numerator, denominator); self.numerator, self.denominator = numerator // div, denominator // div

    #возвращает числитель и знаменатель дроби
    def __call__(self):
        return self.numerator, self.denominator

    #возвращает тип числа(дробное)
    def getType(self):
        return "Number"

    #сложение
    def __add__(self, arg):
        numerator, denominator = arg(); return Number(self.numerator * denominator + numerator * self.denominator, denominator * self.denominator)

    #вычитание
    def __sub__(self, arg):
        numerator, denominator = arg(); return Number(self.numerator * denominator - numerator * self.denominator, denominator * self.denominator)

    #умножение
    def __mul__(self, arg):
        numerator, denominator = arg(); return Number(self.numerator * numerator, self.denominator * denominator)

    #деление
    def __truediv__(self, arg):
        numerator, denominator = arg(); return Number(self.numerator *  denominator, self.denominator * numerator)

    #возведение в степень
    def __pow__(self, arg):
        return PowNumber(self, arg).check()

    #представление дроби в виде строки
    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    #сравнение типов объектов
    def __eq__(self, arg):
        return self.getType() == arg

    #для сокращения дроби
    def nod(self, a, b):
        if b == 0: return a
        else: return self.nod(b, a % b)

    #представление числа в десятичном формате
    def decimal_format(self):
        a, b = self(); return a/b


# объект - число в виде дроби, возведенное в число в виде дроби)
class PowNumber:
    #представление дробного числа в дробной степени. На вход - 2 объекта класса Number
    def __init__(self, number=Number(), power=Number()):
        self.number = number
        self.power = power

    #если объект можно представить в виде дроби, число становится объектом класса Number
    def check(self):
        a, b = self.number.decimal_format(), self.power.decimal_format()
        if a**b == int(a**b): return Number(int(a**b))
        return PowNumber(self.number, self.power)

    #возвращает тип числа(число в степени)
    def getType(self):
        return "PowNumber"

    #сравнение типов объектов
    def __eq__(self, arg):
        if self.getType() == arg.getType():
            if (self.number == arg.number) and (self.power == arg.power): return True
        return False

    #представление числа в десятичном формате
    def decimal_format(self):
        a, b = self.number.decimal_format(), self.power.decimal_format(); return a**b

    #представление числа в степени в строковом представлении
    def __str__(self):
        return f"{self.number}^{self.power}"

    #возвращает основание и показатель степени
    def getValue(self):
        return self.number, self.power


class Group:
    def __init__(self, arg):
        self.arg = arg

