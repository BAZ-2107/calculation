# -*- coding: utf-8 -*-
def mulls(a, massiv=[1]): # разбиение числа на множители
    if a == 1: return massiv
    for i in range(2, a + 1):
        if a%i==0: return mulls(a//i, massiv+[i])

def nod(a, b): # наибольший общий делитель у двух натуральных чисел
    if b==0: return a
    return nod(b, a%b)

isnatural = lambda x: x > 0 and x%1==0

class Natural:
    def __init__(self, number):
        self.number = number
        self.componoud = mulls(number)
        self.format_str = str(number)
        self.type =  "N"

    def __str__(self):
        return self.format_str

    def __add__(self, other):
        result = self.number + other.number
        if isnatural(result): return Natural(result)
        return Integer(result)

    def __mul__(self, other):
        result = self.number * other.number
        if isnatural(result): return Natural(result)
        return Integer(result)

    def __pow__(self, other):
        result = self.number ** other.number
        return Natural(result)

    def __sub__(self, other):
        result = self.number - other.number
        if isnatural(result): return Natural(result)
        return Integer(result) 

    #def truediv(self, other):
        #return Rational(self.number, other.number)

class Integer(Natural):
    def __init__(self, number):
        super().__init__(number)
        self.componoud = mulls(abs(number))
        self.type = "Z"

a = Natural(4)
b = Integer(-3)
c = a*b
print(b.componoud, b.type)