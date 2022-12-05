import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./calculator.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Calculator v1.0.0')
        self.btn_clear_clicked_slot()
        btns = [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
                self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9]

        btn_ops = [self.btn_add, self.btn_sub, self.btn_mul, self.btn_div, self.btn_eql]

        for btn in btns: btn.clicked.connect(self.btn_number_clicked_slot)
        for btn in btn_ops: btn.clicked.connect(self.btn_opcode_clicked_slot)

        self.btn_eql.clicked.connect(self.btn_equal_clicked_slot)
        self.btn_clear.clicked.connect(self.btn_clear_clicked_slot)

    def btn_number_clicked_slot(self):
        btn = self.sender()
        if self.is_first:
            if btn.objectName()[-1] != '0': # 0이 아니면 입력을 받기 시작
                self.is_first = False
            self.lbl_result.setText('')  # 처음입력이 0이면 입력 받지 않음
        self.lbl_result.setText(self.lbl_result.text() + btn.objectName()[-1]) # btn.objectName()[-1] : 인덱싱 마지막을 봄 -> 숫자

    def btn_opcode_clicked_slot(self): #연산자를 누르면
        btn = self.sender()
        if self.opcode == 'div' and float(self.lbl_result.text()) == 0.0:
            self.lbl_result.setText('infinity')
        if self.opcode != None and not self.is_first: # None이면 그냥 패스
            self.btn_equal_clicked_slot()
        self.is_first = True  # 연산자 누른뒤 라벨 초기화
        self.opcode = btn.objectName()[-3:] # btn.objectName()[-3] : 인덱싱 끝에서 3번째부터 끝까지 봄 -> 연산자 이름
        self.number1 = float(self.lbl_result.text()) # 이전에 입력한 수는 저장

    def btn_equal_clicked_slot(self):
        self.is_first = True
        if self.opcode == 'add':
            self.lbl_result.setText(str(self.number1 + int(self.lbl_result.text())))
        elif self.opcode == 'sub':
            self.lbl_result.setText(str(self.number1 - int(self.lbl_result.text())))
        elif self.opcode == 'mul':
            self.lbl_result.setText(str(self.number1 * int(self.lbl_result.text())))
        elif self.opcode == 'div':
            self.lbl_result.setText(str(self.number1 / int(self.lbl_result.text())))
        self.opcode = None

    def btn_clear_clicked_slot(self):
        self.lbl_result.setText('0')
        self.is_first = True #첫자리부터 처음받기위해서
        self.number1 = None #op코드 전까지 입력한 숫자를 저장
        self.opcode = None #op코드를 저장

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())