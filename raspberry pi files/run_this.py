import pandas as pd
import numpy as np
from numpy import asarray
from pathlib import Path
import cv2, pickle, csv, os, sys, re
from PIL import Image, ImageOps
from tools import *
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
import tensorflow as tf


# Чтение таблицы ключевых точек и директории изображении. Указать путь к CSV файлу и изображениям.
csv_file_path = Path("./Training_Project300x200/Training_Project_dataset.csv")
images_dirname = Path("./Training_Project300x200/colored")

# Получения основных данных
SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_count_initail_state, csv_initial_state = get_main_data(csv_file_path, images_dirname, True)


# Подготовка данных (уже писали)
if SHAPE[2] == 3:
    X = np.stack([string2image(Path(os.path.join(images_dirname, image_path))) for image_path in sorted_images]).astype(np.float64)[:, :, :, :]
if SHAPE[2] == 1:
    X = np.stack([string2image(Path(os.path.join(images_dirname, image_path))) for image_path in sorted_images]).astype(np.float64)[:, :, :, np.newaxis]

y = np.vstack(keypoints_df[keypoints_df.columns[2:]].values)
X_train = X / 255


# Подготовка данных (А именно, нормализация данныз для МО)
output_pipe = make_pipeline(
    MinMaxScaler(feature_range=(-1, 1))
)

y_train = output_pipe.fit_transform(y)


# # Для загрузки ранее сохраненной модели
model = keras.models.load_model('model')


# Для тестирования на отдельных изображениях

# Путь к изображению            СЮДА
test_image = cv2.imread("photo1.jpeg")
test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)

reshaped_test_imageI = cv2.resize(test_image, (300, 200))
reshaped_test_image = reshaped_test_imageI.reshape(1, *SHAPE)/255
reshaped_test_image = reshaped_test_image.astype('float32')

predictions = model.predict(reshaped_test_image)
xy_predictions = output_pipe.inverse_transform(predictions).reshape(y.shape[1]//2, 2)
plt.imshow(reshaped_test_imageI)


lameness = False
if xy_predictions[2][1] < xy_predictions[1][1] and xy_predictions[2][1] < xy_predictions[3][1]:
    lameness = True

for i, xy in enumerate(xy_predictions):
    if lameness and i in [1,2,3]:
        plt.plot(xy[0], xy[1], 'r*')
    else:
        plt.plot(xy[0], xy[1], 'b*')

plt.show()
