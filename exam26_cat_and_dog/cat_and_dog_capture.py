import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PIL import Image
from keras.models import load_model
import numpy as np
import cv2 #카메라 모듈
import time

form_window = uic.loadUiType('./cat_and_dog.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = load_model('./cat_dog_83.h5')
        self.path = ('../datasets/cat_dog/train/cat.4.jpg', '')
        self.btn_open.clicked.connect(self.image_open_slot)
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def image_open_slot(self):
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        flag = True
        while flag:
            _, frame = capture.read()
            cv2.imshow('VideoFrame', frame)
            cv2.imwrite('./capture.png', frame)
            time.sleep(1/16)
            key = cv2.waitKey(33)
            if key == 27:
                flag = False
            pixmap = QPixmap('./capture.png')
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
                    self.lbl_pred.setText('고양이일 확률이 {}% 입니다.'.format(
                        ((1 - pred[0][0]) * 100).round(1)
                    ))
                else:
                    self.lbl_pred.setText('강아지일 확률이 {}% 입니다.'.format(
                        ((pred[0][0]) * 100).round(1)
                    ))
            except:
                print('error')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())