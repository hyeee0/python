from PIL import Image
import glob
import numpy as np
from sklearn.model_selection import train_test_split

img_dir = '../datasets/cat_dog/train/' # 이미지 파일이 들어있는 폴더에 가기위한 경로
categories = ['cat', 'dog']
image_w = 64 # 이미지 width 64
image_h = 64 # high 64
pixel = image_h * image_w * 3 # 가로세로 * 3 -> 칼라사진은 곱하기 3
X = []
Y = []
files = None

for idx, category in enumerate(categories):  # cat은 0 dog는 1
    files = glob.glob(img_dir + category + '*.jpg')
    print(category, len(files))
    for i, f in enumerate(files):
        try:
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((image_w, image_h))
            data = np.asarray(img)
            X.append(data)
            Y.append(idx)
            if i % 300 == 0:
                print(category, ':', f)
        except:
            print('error', f)
X = np.array(X)
Y = np.array(Y)
X = X / 255
print(X[0])
print(Y[0])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
xy = (X_train, X_test, Y_train, Y_test)
np.save('../datasets/binary_image_data.npy', xy)

