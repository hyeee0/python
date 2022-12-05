import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./poster_view.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_jaback.clicked.connect(self.btn_slot)
        self.btn_life.clicked.connect(self.btn_slot)
        self.btn_gongjo2.clicked.connect(self.btn_slot)
        self.btn_black.clicked.connect(self.btn_slot)

    def btn_slot(self):
        btn = self.sender()

        self.lbl_jaback.hide()
        self.lbl_life.hide()
        self.lbl_gongjo2.hide()
        self.lbl_black.hide()

        if btn.objectName() == 'btn_jaback': self.lbl_jaback.show()
        elif btn.objectName() == 'btn_life': self.lbl_life.show()
        elif btn.objectName() == 'btn_gongjo2':  self.lbl_gongjo2.show()
        elif btn.objectName() == 'btn_black':  self.lbl_black.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())