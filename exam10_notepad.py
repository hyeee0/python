import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./qt_notepad.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_path = ('제목 없음', '')
        self.title_tail = ' - Qt Notepad v1.0.0'
        self.setWindowTitle(self.file_path[0].split('/')[-1] + self.title_tail)
        self.is_edited = False # 맨 처음에는 편집이 안됐으니깐 False로 초기화
        self.actionSave.triggered.connect(self.action_save_triggered_slot)
        self.actionSave_as.triggered.connect(self.action_save_as_triggered_slot)
        self.actionOpen.triggered.connect(self.action_open_triggered_slot)
        self.actionNew.triggered.connect(self.action_new_triggered_slot)
        self.actionExit.triggered.connect(self.close)

        self.plainTextEdit.textChanged.connect(self.plain_text_changed_slot)

        self.actionRedo.triggered.connect(self.plainTextEdit.redo)
        self.actionPaste.triggered.connect(self.plainTextEdit.paste)
        self.actionCut.triggered.connect(self.plainTextEdit.cut)
        self.actionCopy.triggered.connect(self.plainTextEdit.copy)
        self.actionUndo.triggered.connect(self.plainTextEdit.undo)
        self.actionDelete_2.triggered.connect(self.plainTextEdit.cut)
        self.actionFont.triggered.connect(self.action_font_triggered_slot)
        self.actionAbout.triggered.connect(self.action_about_triggered_slot)

    def action_about_triggered_slot(self):
        QMessageBox.about(self,
                          'Qt Note Pad',
                        '''만든이 : ABC Lab\n버전정보 : 1.0.0
                        ''')


    def action_font_triggered_slot(self):
        font = QFontDialog.getFont()
        print(font)

    def closeEvent(self, QCloseEvent):
        if self.is_edited:
            ans = QMessageBox.question(self, 'notepad', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes:  # Yes가 들어오면 저장
                self.action_save_triggered_slot()  # 파일이 '제목없음'이면 경로를 물어봄
                QCloseEvent.accept()
            elif ans == QMessageBox.No:
                QCloseEvent.accept()
            elif ans == QMessageBox.Cancel:
                QCloseEvent.ignore()
        else:
            QCloseEvent.accept()


    def action_new_triggered_slot(self):
        if self.is_edited:
            ans = QMessageBox.question(self, 'notepad', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes:  # Yes가 들어오면 저장
                self.action_save_triggered_slot()  # 파일이 '제목없음'이면 경로를 물어봄
                self.plain_text_edit_init()
            elif ans == QMessageBox.No:
                self.plain_text_edit_init()
        else:
            self.plain_text_edit_init()

    def plain_text_edit_init(self):
        self.plainTextEdit.setPlainText('')
        self.is_edited = False
        self.plainTextEdit.textChanged.connect(self.plain_text_changed_slot)
        self.file_path = ('제목 없음', '')
        self.setWindowTitle(self.file_path[0].split('/')[-1] + self.title_tail)

    def plain_text_changed_slot(self):
        self.is_edited = True
        self.setWindowTitle('*' + self.file_path[0].split('/')[-1] + self.title_tail)
        self.plainTextEdit.textChanged.disconnect(self.plain_text_changed_slot)

    def action_open_triggered_slot(self):
        if self.is_edited: #수정이 될때
            ans = QMessageBox.question(self, 'notepad', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes:  # Yes가 들어오면 저장
                self.action_save_triggered_slot()  # 파일이 '제목없음'이면 경로를 물어봄
                self.plainTextEdit_init_with_file()
            elif ans == QMessageBox.No:
                self.plainTextEdit_init_with_file()
        else:
            self.plainTextEdit_init_with_file()


    def plainTextEdit_init_with_file(self):
        old_path = self.file_path
        self.file_path = QFileDialog.getOpenFileName(self, 'Save file', 'C:/Users/LG/Desktop/work/python',
                'Text Files(*.txt);;Python Files(*.py);;All files(*.*)')
        print(self.file_path)
        if self.file_path[0]:
            with open(self.file_path[0], 'r') as f:
                document = f.read()
                self.plainTextEdit.setPlainText(document)
                self.setWindowTitle(self.file_path[0].split('/')[-1] + self.title_tail)
                self.is_edited = False #저장을 취소할 경우
                self.plainTextEdit.textChanged.connect(self.plain_text_changed_slot)
        else:
            self.file_path = old_path

    def action_save_triggered_slot(self):
        if self.file_path[0] == '제목 없음':
            self.action_save_as_triggered_slot()
        else:
            with open(self.file_path[0], 'w') as f:
                f.write(self.plainTextEdit.toPlainText())

    def action_save_as_triggered_slot(self):
        old_path = self.file_path
        self.file_path = QFileDialog.getSaveFileName(self, 'Save file', 'C:/Users/LG/Desktop/work/python',
                'Text Files(*.txt);;Python Files(*.py);;All files(*.*)')
        if self.file_path[0]:
            with open(self.file_path[0], 'w') as f:
                f.write(self.plainTextEdit.toPlainText())
            self.setWindowTitle(self.file_path[0].split('/')[-1] + self.title_tail)
            self.is_edited = False
            self.plainTextEdit.textChanged.connect(self.plain_text_changed_slot)
        else:
            self.file_path = old_path
        print(self.file_path)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())