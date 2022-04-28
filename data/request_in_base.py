# -*- coding: utf-8 -*-
import sqlite3


class RequestsInBase: #класс для выполнения запросов в базу данных(по умолчанию "math" в текущей директории)
    name_base = "math"
    con = sqlite3.connect(name_base)
    cur = con.cursor()        

    def changeBase(self, name_base): #если вдруг поменяется директория "math"
        self.name_base = name_base

    def getSections(self): #возвращает список разделов математики
        return [elem[0] for elem in self.cur.execute("SELECT section from sections").fetchall()]

    def getTerms(self): #возвращает список терминов
        return [elem[0] for elem in self.cur.execute("SELECT term from terms").fetchall()]

    def getSectionDescription(self, section): #возвращает описание раздела математики, в виде кортежа
        return self.cur.execute(f"SELECT description from sections WHERE section = '{section}' ").fetchone()

    def getSectionId(self, section): #возвращает описание раздела математики, в виде кортежа
        return self.cur.execute(f"SELECT id from sections WHERE section = '{section}' ").fetchone()    

    def getTermDescription(self, term): #возвращает описание термина, в виде кортежа
        return self.cur.execute(f"SELECT description from terms WHERE term = '{term}' ").fetchone()

    def getSectionFromTerm(self, term): #возвращает раздел математики, к которому относится данный термин, в виде кортежа
        return self.cur.execute(f"""SELECT section from sections WHERE id = (SELECT section FROM terms WHERE term = "{term}" ) """).fetchone()

    def getTermsFromSection(self, section): #возвращает список терминов, которые относятся к данному разделу
        return [elem[0] for elem in self.cur.execute(f"""SELECT term from terms WHERE section = (SELECT id FROM sections WHERE section = "{section}" ) """).fetchall()]


class AddInBase(RequestsInBase): #класс унаследован от класса RequestsInBase
    def addInTerms(self, **kwargs): #добавляет термин или возвращает сообщение об ошибке
        if kwargs["term"] == "": return "термин не может быть пустым"
        if kwargs["term"] in self.getTerms() and kwargs["section"] == self.getSectionFromTerm(kwargs["term"])[0]: return f'термин "{kwargs["term"]}" уже существует в разделе "{kwargs["section"]}"'
        if kwargs["section"] not in self.getSections(): return f'раздел "{kwargs["section"]} не существует'
        if kwargs["description"] == "": return "Описание не может быть пустым"
        self.cur.execute(f'INSERT INTO terms VALUES("{kwargs["term"]}", "{kwargs["description"]}", {self.getSectionId(kwargs["section"])[0]})')
        self.con.commit()
        return f'Термин "{kwargs["term"]}" записан в раздел "{kwargs["section"]}"'

    def addInSections(self, **kwargs): #добавляет раздел или возвращает сообщение об ошибке
        if kwargs["section"] == "": return "Раздел не может быть пустым"
        if kwargs["section"] in self.getSections(): return f'Раздел "{kwargs["section"]}" уже существует'
        if kwargs["description"] == "": return "Описание не может быть пустым"
        self.cur.execute(f'INSERT INTO sections VALUES(NULL, "{kwargs["section"]}", "{kwargs["description"]}")')
        self.con.commit()
        return f'Раздел "{kwargs["section"]}" добавлен'

print(AddInBase().addInSections(section="qwew", description="wer"))