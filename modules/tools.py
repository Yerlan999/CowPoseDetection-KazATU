import pandas as pd
import numpy as np
from numpy import asarray
from itertools import tee
from pathlib import Path
import cv2, pickle, csv, os, sys, re, math, inspect
from PIL import Image, ImageOps, ImageEnhance
import matplotlib.pyplot as plt
from skimage.util import random_noise



class AugmentApply():

    last_image_index = None
    curr_img_count = None
    first_time = True
    initial_images_list = None
    initail_df = None

    def __init__(self, list_of_methods, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path, images_count_initail_state, csv_initial_state):

        self.list_of_methods = list_of_methods
        self.SHAPE = SHAPE
        self.current_wd = current_wd
        self.keypoints_df = keypoints_df
        self.sorted_images = sorted_images
        self.images_dirname = images_dirname
        self.csv_file_path = csv_file_path
        self.last_image_index = last_image_index
        self.curr_img_count = curr_img_count

        if AugmentApply.first_time:
            AugmentApply.last_image_index = last_image_index
            AugmentApply.curr_img_count = curr_img_count
            AugmentApply.initial_images_list = sorted_images
            AugmentApply.initial_df = keypoints_df
            AugmentApply.first_time = False
        else:
            AugmentApply.last_image_index = images_count_initail_state
            AugmentApply.curr_img_count = images_count_initail_state
            self.keypoints_df = AugmentApply.initial_df

        backup_df = pd.read_csv(csv_file_path)

        # Clearing images folder to initial state before applying/reapplying Data Augmentation
        self.sorted_images = AugmentApply.initial_images_list

        for i, image in enumerate(sorted_images):
            if i > images_count_initail_state:
                os.remove(os.path.join(self.images_dirname, image))
        with open(csv_file_path, "w", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(csv_initial_state.columns))
        with open(csv_file_path, "a", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_initial_state.values.tolist():
                writer.writerow(row)

        AugmentApply.last_image_index = images_count_initail_state
        AugmentApply.curr_img_count = images_count_initail_state
        self.last_image_index = images_count_initail_state
        self.curr_img_count = images_count_initail_state

        # Applying Data Augmentation
        try:
            for method in list_of_methods:
                method.apply_me(self.SHAPE, AugmentApply.last_image_index, AugmentApply.curr_img_count, self.current_wd, self.keypoints_df, self.sorted_images, self.images_dirname, self.csv_file_path)
        except Exception as error:
            print("Произошла ошибка. Восстановление исходных данных...")
            print(error)

            for i, image in enumerate(sorted_images):
                if i > self.last_image_index:
                    os.remove(os.path.join(self.images_dirname, image))

            with open(csv_file_path, "w", newline='') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(list(backup_df.columns))
            with open(csv_file_path, "a", newline='') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in backup_df.values.tolist():
                    writer.writerow(row)
            AugmentApply.last_image_index = self.last_image_index
            AugmentApply.curr_img_count = self.curr_img_count
        else:
            print(" ***** Готово! ***** ")







class RotateImages():

    def __init__(self, angle):
        assert type(angle) == int, "Должно быть целое число!"
        self.angle = int(angle)

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение вращения изображении на " + str(self.angle) + " градусов")
        cancel = rotateCSVfile(self.angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        if not cancel:
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
        print("Применение переворота изображении")
        flipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        flipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class ShiftImages():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение смещения изображении по координате х на " + str(self.x) + " и по координате у на " + str(self.y))
        cancel = shiftCSVfile(self.x, self.y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        if not cancel:
            shiftImage(self.x, self.y, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class MirrorFlipImages():

    def __init__(self, ):
        pass

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение отзеркаливания + переворота изображении")
        mirrorflipCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        mirrorflipImage(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class BlurImages():

    def __init__(self, kernel):
        self.kernel = kernel

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение размытия изображении на " + str(self.kernel))
        blurCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        blurImage(self.kernel, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class NoiseImages():

    def __init__(self, amount):
        self.amount = amount

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Применение шума изображении на " + str(self.amount))
        noiseCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        noiseImage(self.amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class BrightenImages():

    def __init__(self, amount):
        self.amount = amount

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Изменение яркости изображении на " + str(self.amount))
        brightenCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        brightenImage(self.amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class ContrastImages():

    def __init__(self, amount):
        self.amount = amount

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Изменение контрастности изображении на " + str(self.amount))
        contrastCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        contrastImage(self.amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)


class SaturationImages():

    def __init__(self, amount):
        self.amount = amount

    def apply_me(self, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
        print("Изменение насыщенности изображении на " + str(self.amount))
        saturationCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)
        saturationImage(self.amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path)






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


def blurImage(kernel, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    if (kernel % 2) == 0:
        kernel += 1
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        blurred_image = cv2.GaussianBlur(image, (kernel, kernel), cv2.BORDER_DEFAULT)
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', blurred_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def noiseImage(amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        noise_img = random_noise(image, mode='s&p',amount=amount)
        noised_image = np.array(255*noise_img, dtype = 'uint8')
        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', noised_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def brightenImage(amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(color_coverted)

        #image brightness enhancer
        enhancer = ImageEnhance.Brightness(pil_image)
        im_output = enhancer.enhance(amount)

        numpy_image=np.array(im_output)
        brightened_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', brightened_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def contrastImage(amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(color_coverted)

        #image brightness enhancer
        enhancer = ImageEnhance.Contrast(pil_image)
        im_output = enhancer.enhance(amount)

        numpy_image=np.array(im_output)
        contrasted_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', contrasted_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)


def saturationImage(amount, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):
    """ Функция для вращения изображении """
    for image_name in sorted_images:
        image = cv2.imread(os.path.join(images_dirname, image_name))
        height, width = image.shape[:2]
        center = (width/2, height/2)
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(color_coverted)

        #image brightness enhancer
        enhancer = ImageEnhance.Color(pil_image)
        im_output = enhancer.enhance(amount)

        numpy_image=np.array(im_output)
        saturated_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

        os.chdir(images_dirname)
        cv2.imwrite("cow" + str(AugmentApply.curr_img_count+1) +'.jpg', saturated_image)
        AugmentApply.curr_img_count += 1
    os.chdir(current_wd)








def rotateCSVfile(angle, SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    rot_keypoints_df = keypoints_df.copy()
    lost_points_count = 0

    # Lost point counter
    for row in range(len(keypoints_df.index)):
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            new_points = rotatePoint(center, (point_x, point_y), angle)
            if new_points[0] < 0 or new_points[1] < 0 or new_points[0] > width or new_points[1] > height:
                lost_points_count += 1

    if lost_points_count > 0:
        proceed = str(input("Количество потерянных точек при вращении изображении на " + str(angle) + " градусов: " + str(lost_points_count) + " Все равно применить? [Да/Нет]"))
        if proceed.strip().lower() == "нет":
            return True

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
    lost_points_count = 0

    # Lost point counter
    for row in range(len(keypoints_df.index)):
        for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
            point_x = keypoints_df.iloc[row,2:][pair[0]]
            point_y = keypoints_df.iloc[row,2:][pair[1]]
            new_points = (point_x + x, point_y + y)
            if new_points[0] < 0 or new_points[1] < 0 or new_points[0] > width or new_points[1] > height:
                lost_points_count += 1

    if lost_points_count > 0:
        proceed = str(input("Количество потерянных точек при смещении изображении по х на " + str(x) + " и по у на " + str(y) + ": " + str(lost_points_count) + " Все равно применить? [Да/Нет]"))
        if proceed.strip().lower() == "нет":
            return True

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


def blurCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    blu_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        blu_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        blu_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in blu_keypoints_df.values.tolist():
            writer.writerow(row)


def noiseCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    noi_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        noi_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        noi_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in noi_keypoints_df.values.tolist():
            writer.writerow(row)


def brightenCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    bri_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        bri_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        bri_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in bri_keypoints_df.values.tolist():
            writer.writerow(row)


def contrastCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    con_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        con_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        con_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in con_keypoints_df.values.tolist():
            writer.writerow(row)


def saturationCSVfile(SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_dirname, csv_file_path):

    height, width = SHAPE[:2]
    center = (width/2, height/2)
    sat_keypoints_df = keypoints_df.copy()

    for row in range(len(keypoints_df.index)):
        sat_keypoints_df.iat[row, 1] = "cow" + str(AugmentApply.last_image_index+1) + ".jpg"
        sat_keypoints_df.iat[row, 0] = AugmentApply.last_image_index + 1

        AugmentApply.last_image_index += 1

    with open(csv_file_path, "a", newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in sat_keypoints_df.values.tolist():
            writer.writerow(row)





# Функция для специальной парной итерации
def pairwise_2(iterable):
    a = iter(iterable)
    return zip(a, a)





def get_main_data(csv_file_path, images_dirname, first):

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
    images_count_initail_state = len(sorted_images) - 1
    csv_initial_state = keypoints_df

    if first:
        csv_initial_state = keypoints_df
        return SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images, images_count_initail_state, csv_initial_state
    else:
        return SHAPE, last_image_index, curr_img_count, current_wd, keypoints_df, sorted_images



def show_cowannot(image_index, keypoints_df, images_dirname, sorted_images):
    # Просмотр изображении с аннотациями по номеру.
    keypoint_cols = list(keypoints_df.columns)[2:]
    xy = keypoints_df.iloc[image_index][keypoint_cols].values.reshape((int(len(keypoints_df.columns[2:])/2), 2))
    plt.plot(xy[:, 0], xy[:, 1], 'ro')
    plt.imshow(string2image(Path(os.path.join(images_dirname, sorted_images[image_index]))), cmap='gray')


def my_congrats2U():
    print("Желаю вам, прожить вместе такую жизнь, чтоб о ней написали книгу, а она взяла и стала бестселлером. \U0001F60E")
    print("Привет Кингу от меня \U0001F436")
