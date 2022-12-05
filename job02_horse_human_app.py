import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PIL import Image
from keras.models import load_model
import numpy as np

form_window = uic.loadUiType('./horse_or_human.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = load_model('./datasets/horse-or-human/horse-or-human_model.h5')
        self.path = ('./datasets/horse-or-human', '')
        self.btn_open.clicked.connect(self.image_opne_slot)

    def image_opne_slot(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open File',
          './datasets/horse-or-human', 'Image Files(*.jpg;*.png);;All Files(*.*)')
        if self.path[0]:
            pixmap = QPixmap(self.path[0])
            self.lbl_image.setPixmap(pixmap)
            try:
                img = Image.open(self.path[0])
                img = img.convert('RGB')
                img = img.resize((64, 64))
                data = np.asarray(img)
                data = data / 255
                data = data.reshape(1, 64, 64, 3)
                pred = self.model.predict(data)
                print(pred)
                if pred < 0.5:
                    self.lbl_pred.setText('말일 확률이 {}% 입니다.'.format(
                       ((1 - pred[0][0]) * 100).round(1)
                    ))
                else:
                    self.lbl_pred.setText('사람일 확률이 {}% 입니다.'.format(
                       ((pred[0][0]) * 100).round(1)
                    ))
            except:
                print('error')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())