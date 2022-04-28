# -*- coding: utf-8 -*-
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QDialog, QTextEdit, QComboBox
from PyQt5 import uic
from database_actions import RequestsInBase, AddInBase, DeleteOfBase, EditBase

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("call_with_database.ui", self)
        #массивы с объектами
        self.for_new_term = [self.label, self.term, self.label_2, self.term_description, 
                             self.label_5, self.sections, self.pushButton]
        self.for_new_section = [self.label_6, self.section, self.label_7, self.section_description, 
                             self.pushButton]
        self.for_del_term = [self.label_4, self.terms, self.label, self.term,
                             self.label_2, self.term_description, 
                             self.label_3, self.section_name, self.pushButton]
        self.for_del_section = [self.label_5, self.sections, self.label_6, self.section,
                             self.label_7, self.section_description, self.pushButton]        
        
        #заполняем термины и разделы в ComboBox
        self.terms.addItems(RequestsInBase().getTerms())
        self.sections.addItems(RequestsInBase().getSections())

        self.terms.activated.connect(self.term_changed)
        self.sections.activated.connect(self.section_changed)
        #при выборе термина или раздела вызывается метод для 
        #при переходе на какую-нибудь вкладку(пример: редактировать -> термин)
        """self.search_term.triggered.connect(self.example)
        self.search_section.triggered.connect(self.example)"""
        self.add_term.triggered.connect(self.add_term_to_base)
        self.add_section.triggered.connect(self.add_section_to_base)
        """
        self.del_term.triggered.connect(self.del_term_of_base)
        self.del_section.triggered.connect(self.del_section_of_base)
        self.change_term.triggered.connect(self.example)
        self.change_section.triggered.connect(self.example)
        """
        #нажатие на кнопку
        self.pushButton.clicked.connect(self.control)
    
    def section_changed(self):
        if self.sections.actions():
            self.section.setText(self.sections.currentText()); section_description.setText(RequestsInBase().getSectionDescription(self.sections.currentText()))
            self.terms.clear(); self.terms.addItems(RequestsInBase().getTermsFromSection(self.sections.currentText()))
    
    def term_changed(self):
        if self.terms.actions() and self.sections.actions():
            if self.terms.currentText() in RequestsInBase().getTermsFromSection(self.sections.currentText()):
                self.term.setText(self.terms.currentText());
                self.term_description.setText(RequestsInBase().getTermDescription(self.terms.currentText(), self.sections.currentText()))
                self.section_name.setText(self.sections.currentText())
    
    def del_section_of_base(self):
        self.pushButton.setText("Удалить раздел"); self.section.setDisabled(True); self.section_description.setDisabled(True)
        for elem in self.for_new_term + self.for_del_term + self.for_new_section: elem.hide()
        for elem in self.for_del_section: elem.show()
        sections = RequestsInBase().getSections(); self.sections.clear()
        if not sections: self.statusBar().showMessage("Все разделы уже удалены"); self.pushButton.setDisabled(True)
        else: self.sections.addItems(sections); self.pushButton.setEnabled(True)       
        
    def control(self):
        if self.pushButton.text() == "Добавить термин":
            self.statusBar().showMessage(AddInBase().addInTerms(term=self.term.text(), description=self.term_description.toPlainText(), section=self.sections.currentText()))
        elif self.pushButton.text() == "Добавить раздел":
            self.statusBar().showMessage(result = AddInBase().addInSections(section=self.section.text(), description=self.section_description.toPlainText()))
        elif self.pushButton.text() == "Удалить раздел":
            self.statusBar().showMessage(DeleteOfBase().deleteOfSections(section=self.section.text())); self.del_section_of_base()
        elif self.pushButton.text() == "Удалить термин": self.statusBar().showMessage(DeleteOfBase().deleteOfTerms(section=self.section.text())); self.del_term_of_base()
        
        self.terms.clear(); self.terms.addItems(RequestsInBase().getTerms())
        self.sections.clear(); self.sections.addItems(RequestsInBase().getSections())        
            
    def add_term_to_base(self):
        self.pushButton.setText("Добавить термин"); self.term.setEnabled(True); self.term_description.setEnabled(True)
        for elem in self.for_new_section + self.for_del_term + self.for_del_section: elem.hide()
        for elem in self.for_new_term: elem.show()
        self.term.clear(); self.term_description.clear()
        if self.sections.currentText() == "": self.statusBar().showMessage("Невозможно создать термин, пока не существуют разделы"); self.pushButton.setDisabled(True)
        else: self.pushButton.setEnabled(True)
    
    def add_section_to_base(self):
        self.pushButton.setEnabled(True); self.pushButton.setText("Добавить раздел"); self.section.setEnabled(True); self.section_description.setEnabled(True)
        for elem in self.for_new_term + self.for_del_term + self.for_del_section: elem.hide()
        for elem in self.for_new_section: elem.show()
        self.section.clear(); self.section_description.clear()
    
    def del_term_of_base(self):
        self.pushButton.setDisabled(True)
        self.pushButton.setText("Удалить термин"); self.term.setEnabled(True); self.term_description.setEnabled(True)
        for elem in self.for_new_section + self.for_del_term + self.for_del_section: elem.hide()
        for elem in self.for_new_term: elem.show()
        self.term.clear(); self.term_description.clear(); self.section_name.clear()
        self.term.setDisabled(True); self.term_description.setDisabled(True); self.section_name.setDisabled(True)
        if self.sections.currentText() == "": self.statusBar().showMessage("Не найдено разделов")
        elif self.terms.currentText() == "": self.statusBar().showMessage("Не найдено терминов")
        else: self.pushButton.setEnabled(True)
        
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)   
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())