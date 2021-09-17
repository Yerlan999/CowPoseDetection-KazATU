import pandas as pd
import numpy as np
from numpy import asarray
from itertools import tee
from pathlib import Path
import cv2, pickle, csv, os, sys, re, math, inspect
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


class AugmentApply():

    last_image_index = None
    curr_img_count = None

    def __init__(self, list_of_methods, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

        self.list_of_methods = list_of_methods
        self.SHAPE = SHAPE

        AugmentApply.last_image_index = last_image_index
        AugmentApply.curr_img_count = curr_img_count

        self.current_wd = current_wd
        self.keypoints_df = keypoints_df
        self.sorted_images = sorted_images
        self.images_dirname = images_dirname
        self.csv_file_path = csv_file_path

        for method in list_of_methods:
            if not inspect.isclass(method.__class__):
                raise ValueError("Ошибка! Проверь правописание методов.")

        print("Просто жди...")
        for method in list_of_methods:
            method.apply_me(self.SHAPE, AugmentApply.last_image_index, AugmentApply.curr_img_count, self.current_wd, self.keypoints_df, self.sorted_images, self.images_dirname, self.csv_file_path)
        print("Готово!")



class RotateImages():

    def __init__(self, angle):
        assert type(angle) == int, "Должно быть целое число!"
        self.angle = int(angle)

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение вращения изображении на " + str(self.angle) + " градусов")
        rotateCSVfile(self.angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        rotateImage(self.angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class MirrorImages():

    def __init__(self, ):
        pass

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение отзеркаливания изображении")
        mirrorCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        mirrorImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class FlipImages():

    def __init__(self, ):
        pass

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение перворота изображении")
        flipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        flipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class ShiftImages():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение смещения изображении по координате х на " + str(self.x) + " и по координате у на " + str(self.y))
        shiftCSVfile(self.x, self.y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        shiftImage(self.x, self.y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class MirrorFlipImages():

    def __init__(self, ):
        pass

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение отзеркаливания + переворота изображении")
        mirrorflipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        mirrorflipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)





# Функции для просмотра изображении
def string2image(jpeg_image_path):
    image = Image.open(jpeg_image_path)
    img_array = np.asarray(image)
    return img_array


def plot_cow(image):
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(string2image(image), cmap='gray')


def rotatePoint(centerPoint, point, angle):
    """ Функция для вращения точки относительно другой точки(в данном случае, центра картинки) """
    angle = math.radians(-angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point


# Создание и сохранение перевернутых изображении
def rotateImage(angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
        rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', rotated_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def mirrorImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        mirrored_image = cv2.flip(image, 1)
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', mirrored_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def flipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        mirrored_image = cv2.flip(image, 0)
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', mirrored_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def shiftImage(x, y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        M = np.float32([[1, 0, x],[0, 1, y]])
        shifted_image = cv2.warpAffine(image, M, (width, height))
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', shifted_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def mirrorflipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        mirroredflipped_image = cv2.flip(image, -1)
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', mirroredflipped_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)



def rotateCSVfile(angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    rot_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        rot_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        rot_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            new_points = rotatePoint(center, (point_x, point_y), angle)
            if new_points[0] < 0 or new_points[1] < 0 or new_points[0] > width or new_points[1] > height:
                rot_keypoints_df.iat[row,pair[0]+2] = 0
                rot_keypoints_df.iat[row,pair[1]+2] = 0
            else:
                rot_keypoints_df.iat[row,pair[0]+2] = new_points[0]
                rot_keypoints_df.iat[row,pair[1]+2] = new_points[1]

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rot_keypoints_df.values.tolist():
            writer.writerow(row)


def mirrorCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    mir_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        mir_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        mir_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            mir_keypoints_df.iat[row,pair[0]+2] = width - point_x

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in mir_keypoints_df.values.tolist():
            writer.writerow(row)

def flipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    fli_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        fli_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        fli_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            fli_keypoints_df.iat[row,pair[1]+2] = height - point_y

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in fli_keypoints_df.values.tolist():
            writer.writerow(row)


def shiftCSVfile(x, y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    shi_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        shi_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        shi_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            new_points = (point_x + x, point_y + y)
            if new_points[0] < 0 or new_points[1] < 0 or new_points[0] > width or new_points[1] > height:
                shi_keypoints_df.iat[row,pair[0]+2] = 0
                shi_keypoints_df.iat[row,pair[1]+2] = 0
            else:
                shi_keypoints_df.iat[row,pair[0]+2] = new_points[0]
                shi_keypoints_df.iat[row,pair[1]+2] = new_points[1]

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in shi_keypoints_df.values.tolist():
            writer.writerow(row)


def mirrorflipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    mirfli_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        mirfli_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        mirfli_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            mirfli_keypoints_df.iat[row,pair[0]+2] = width - point_x
            mirfli_keypoints_df.iat[row,pair[1]+2] = height - point_y

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in mirfli_keypoints_df.values.tolist():
            writer.writerow(row)


# Функция для специальной парной итерации
def pairwise_2(iterable):
    a = iter(iterable)
    return zip(a, a)



def get_main_data(csv_file_path, images_dirname):

    keypoints_df = pd.read_csv(csv_file_path)

    images_ext = re.compile(".*(.jpg|.jpeg)")

    filtered = list(filter(images_ext.match, os.listdir(images_dirname)))
    try:
        sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))
    except:
        try:
            sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][2:]))
        except:
            sorted_images = sorted(filtered)


    # Получение разрешения входных изображении (ширина, высота, кол.каналов)
    image = Image.open(Path(os.path.join(images_dirname, sorted_images[0])))
    img_array = np.asarray(image)
    SHAPE = (image.size[1], image.size[0], image.layers)
    last_image_index = len(sorted_images) - 1
    curr_img_count = len(sorted_images) - 1
    current_wd = os.getcwd()

    return SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images


def show_cowannot(image_index, keypoints_df, images_dirname, sorted_images):
    # Просмотр изображении с аннотациями по номеру.
    keypoint_cols = list(keypoints_df.columns)[2:]
    xy = keypoints_df.iloc[image_index][keypoint_cols].values.reshape((int(len(keypoints_df.columns[2:])/2), 2))
    plt.plot(xy[:, 0], xy[:, 1], 'ro')
    plt.imshow(string2image(Path(os.path.join(images_dirname, sorted_images[image_index]))), cmap='gray')
