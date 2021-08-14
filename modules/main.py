from tkinter import *
from tkinter import messagebox, filedialog

from tkinter import ttk  # Normal Tkinter.* widgets are not themed!
from ttkthemes import ThemedTk

import cv2, os, csv, pickle
from PIL import ImageTk, Image, ImageOps
from pathlib import Path
import numpy as np
import pandas as pd
from time import sleep


background_color = "#bdb7b1"
main_label_color = "#adb5bd"
labels_color = "#ccc5b9"
start_button_color = "#adb5bd"
entry_color = "#eaefef"


def donothing():
    help_root = ThemedTk(theme="equilux")
    help_root.geometry("600x200")
    help_frame = ttk.Frame(help_root)

    ttk.Label(help_frame, text="Расположите в одной папке: папку 'config', папку с изображениями и значок программы!", anchor=CENTER).pack(side=TOP, fill=BOTH, expand=True)
    ttk.Label(help_frame, text="После начала проекта не рекомендуется менять содержание папки с изображениями!", anchor=CENTER).pack(side=BOTTOM, fill=BOTH, expand=True)
    help_frame.pack(side=LEFT, fill=BOTH, expand=True)
    help_root.mainloop()


KEY_POINTS = [

    "L_eye",
    "R_eye",
    "L_ear",
    "R_ear",
    "Nose",
    "Throat",
    "Tail",
    "withers",
    "L_F_elbow",
    "R_F_elbow",
    "L_B_elbow",
    "R_B_elbow",
    "L_F_knee",
    "R_F_knee",
    "L_B_knee",
    "R_B_knee",
    "L_F_paw",
    "R_F_paw",
    "L_B_paw",
    "R_B_paw",

]


AXES = ["x", "y"]


def write_config2db(dict_of_data):

    pickle_out = open(Path(os.path.join("config", "db.pickle")),"wb")
    pickle.dump(dict_of_data, pickle_out)
    pickle_out.close()

def read_configfdb():
    pickle_in = open(Path(os.path.join("config", "db.pickle")),"rb")
    return pickle.load(pickle_in)

def on_closing():
    if messagebox.askokcancel("Выход из программы", "Вы действительно хотите выйти?"):
        root.destroy()

state = True
def disable_entries():
    global state

    main_menu = [
        img_height_entry, img_width_entry,
        dir_entry, select_button, proj_entry, add_entry
    ]

    if state:
        for i in main_menu:
            try:
                i.config(state='disabled')
                i['state'] = 'disabled'
            except:
                continue
        state = False
    else:
        for i in main_menu:
            try:
                i.config(state='normal')
                i['state'] = 'normal'
            except:
                continue
        state = True


class KeyPointsSuperStack():

    def __init__(self):
        self.data2load = dict()
        self.stack = []

    def update_dict(self, key, value):
        self.data2load.update({key: value})

    def load_dict(self):
        return self.data2load

    def append(self, keypoint):
        self.stack.append(keypoint)


    def pop(self):
        if len(self.stack) > 0:
            self.stack.pop()

    def get_keypoints(self):
        return self.stack

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1]


    def length(self):
        return len(self.stack)


def validate_numbers(index, numbers):
    return globals()["pattern"].match(numbers) is not None


def validate_letters(index, numbers):
    return globals()["pattern_a"].match(numbers) is not None


def add_keypoint(event):

    if len(added_title.get().strip().replace(" ", "_")):

        if kp_counter.col_index == 0:
            row = kp_counter.step_up()
        label = ttk.Label(root, text=added_title.get(), width=60, anchor=CENTER)
        col = 0 if kp_counter.col_index == 0 else 2
        label.grid(row=kp_counter.current_kp+8, column=col, columnspan=2, sticky="EWNS", padx=1, pady=1)
        kp_counter.add_kp(label)
        add_entry.delete(0, 'end')


def dirinput():
    dirpath = Path(filedialog.askdirectory())
    dir_entry.delete(0, 'end')
    dir_entry.insert(END, dirpath) # add this


class KPCounter():

    def __init__(self):
        self.current_kp = 0
        self.list_of_kps = []
        self.col_index = 0

    def step_up(self):
        self.current_kp += 1
        return self.current_kp

    def step_down(self):
        if self.current_kp > 1 and self.col_index == 1:
            self.current_kp -= 1
        return self.current_kp


    def reset(self):
        self.current_kp = 0
        return self.current_kp

    def add_kp(self, kp):
        self.list_of_kps.append(kp)
        if self.col_index == 0:
            self.col_index = 1
        else:
            self.col_index = 0

    def delete_last_kp(self):
        if len(self.list_of_kps) > 0:
            self.list_of_kps[-1].destroy()
            self.list_of_kps.pop()
        if self.current_kp > 0:
            self.step_down()
        if self.col_index == 0:
            self.col_index = 1
        else:
            self.col_index = 0



class LabelCounter():

    def __init__(self, labels=None):
        self.labels = labels
        self.current_label = 0

    def step_up(self):
        if self.current_label < len(self.labels):
            self.current_label += 1
        return self.current_label

    def step_down(self):
        if self.current_label > 0:
            self.current_label -= 1
        return self.current_label

    def reset(self):
        self.current_label = 0
        self.thresh = True
        return self.current_label

    def get_current_label_name(self):
        try:
            text = self.labels[self.current_label-1]
        except IndexError:
            text = False
        return text

    def lenght(self):
        return len(self.labels)

    def show_current_label(self):
        try:
            text = self.labels[self.current_label]
        except IndexError:
            text = "Готово!"
        try:
            kp_label.destroy()
        except:
            kp_label = ttk.Label(root, text=text, width=1000, anchor=CENTER)
            kp_label.grid(row=0, column=0, columnspan=4, sticky="EWNS", pady=10)
        if text == "Готово!":
            return False
        else:
            return True


class ImageCounter():
    def __init__(self, total=None):
        self.total = total
        self.current_image = 0

    def step_up(self):
        if self.current_image < self.total:
            self.current_image += 1
        return self.current_image

    def step_down(self):
        if self.current_image > 0:
            self.current_image -= 1
        return self.current_image



def adding_more_args(func):
    def wrapper(*args, **kwargs):
        result = func(*args, images_holder, key_points_holder, keypoint_stack, **kwargs)
    return wrapper


def invisible_button(image_class, keypoint_class):
    label_counter.step_up()

    if label_counter.thresh:
        keypoint_stack.update_dict(label_counter.get_current_label_name(), (0, 0))
        keypoint_stack.append(0)

    if not label_counter.show_current_label():
        label_counter.thresh = False
    else:
        label_counter.thresh = True


@adding_more_args
def undo_keypoint(event, image_class, keypoint_class, keypoint_stack):

    if intro:
        if kp_counter.list_of_kps:
            kp_counter.delete_last_kp()
    else:
        label_counter.step_down()
        label_counter.show_current_label()
        image_class.canvas.delete(keypoint_stack.peek())
        keypoint_stack.pop()
        label_counter.thresh = True

@adding_more_args
def next_imageKeyPress(event, image_class, keypoint_class, keypoint_stack):

    try:
        if image_class.image_counter_class.current_image < len(image_class.images_list):

            if len(keypoint_stack.stack) == len(user_def_keypoints):

                config = {
                    "image_index": image_class.image_counter_class.current_image+1,  # !!!
                    "original_images_folder": user_def_images_folder,
                    "project_folder_path": image_class.project_dir_path,
                    "dataset_path": dataset_path,
                    "image_size": image_class.image_size,
                    "key_points_name": user_def_keypoints,
                }
                write_config2db(config)

                with open(dataset_path, "a", newline='') as file:
                    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([image_class.image_counter_class.current_image, Path(image_class.current_image_path).name] + list(i for t in keypoint_stack.data2load.values() for i in t))


                # IMAGES SAVING HERE !!!!

                os.chdir(Path(os.path.join(image_class.project_dir_path.stem, "colored")))
                image_to_save = Image.open(image_class.current_image_path).convert('RGB').resize((image_class.image_size[0], image_class.image_size[1]), Image.ANTIALIAS)
                image_to_save.save("cow"+str(image_class.image_counter_class.current_image)+".jpeg")
                os.chdir("..")
                os.chdir("grayscaled")
                ImageOps.grayscale(image_to_save).save("cow"+str(image_class.image_counter_class.current_image)+".jpeg")
                os.chdir("..")
                os.chdir("..")

                next_image_index = image_class.image_counter_class.step_up() # !!! HERE LIES THE PROBLEM
                image_class.draw_image(next_image_index)
                label_counter.reset()
                label_counter.show_current_label()

                keypoint_stack.stack = []

    except AttributeError as attrerror:
        print(attrerror)



def adding_canvas(func):
    def wrapper(*args, **kwargs):
        result = func(*args, 4, images_holder, **kwargs)
    return wrapper



def start_annotation(dirname, image_class, keypoint_class):
    global intro, label_counter, keypoint_stack, grayscaled, user_def_keypoints, dataset_path, user_def_images_folder
    answer = messagebox.askyesno(title="Внимение!", message="Вы действительно хотите начать процесс аннотации изображении?")
    if answer == False: return;

    contin_last_session = last_session_var.get()


    if not contin_last_session:
        # STARTING NEW PROJECT

        project_name = proj_entry.get().strip().replace(" ", "_")

        if not project_name:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Пожалуйста, введите название проекта")
            return

        try:
            height, width = int(img_height_entry.get()), int(img_width_entry.get())
        except:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Пожалуйста, введите данные ширины и высоты изображении")
            return


        if not dirname or not os.path.isdir(dirname) or dirname in [".", "/", "\\"]:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Пожалуйста, введите путь к папке с изображениями")
            return


        filtered = list(filter(images_ext.match, os.listdir(dirname)))

        try:
            sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))
        except:
            try:
                sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][2:]))
            except:
                sorted_images = sorted(filtered)


        if not os.path.isdir(dirname) or not sorted_images:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Пожалуйста, введите путь к папке с изображениями")
            return

        if len(kp_counter.list_of_kps) < 1:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Пожалуйста, введите ключевые точки")
            return

        user_def_images_folder = Path(os.path.join(os.getcwd(), Path(Path(dirname).stem)))
        project_full_path = Path(os.path.join(os.getcwd(), Path(project_name)))

        if not os.path.isdir(project_name):
            os.mkdir(project_name)
            os.chdir(project_name)
            os.mkdir("grayscaled")
            os.mkdir("colored")
            os.chdir("..")
        dataset_path = Path(os.path.join(project_name, f"{project_name}_dataset.csv"))


        intro = False
        user_def_keypoints = []

        for item in main_menu:
            item.destroy()
        for kp in kp_counter.list_of_kps:
            user_def_keypoints.append(kp.cget("text").lower().strip().replace(" ", "_"))
            kp.destroy()


        label_counter = LabelCounter(user_def_keypoints)
        label_counter.thresh = True


        label_counter.show_current_label()

        invis_kp_button = ttk.Button(root, text="Невидимая ключевая точка", width=1000, cursor="hand2", command=lambda:invisible_button(image_class, keypoint_class))
        invis_kp_button.grid(row=2, column=0, columnspan=2, sticky="EWNS")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        if width > screen_width or width+50 > screen_width:
            width=screen_width-50
        if height > screen_height or height+200 > screen_height:
            height=screen_height-200


        num_of_images = len(sorted_images)

        image_counter = ImageCounter(num_of_images)
        image_class.image_size = (width, height)
        current_image_path = os.path.join(dirname, sorted_images[0])
        img = ImageTk.PhotoImage(Image.open(current_image_path).convert('RGB').convert('RGB').resize((width, height), Image.ANTIALIAS))
        image_class.project_dir_path = project_full_path
        image_class.image_counter_class = image_counter
        image_class.current_image_path = current_image_path
        image_class.current_image_object = img
        image_class.images_folder_path = user_def_images_folder
        image_class.images_list = sorted_images

        canvas = Canvas(root, cursor="hand2", bd=3)
        canvas.config(width=width, height=height)

        first_imge_on_canvas = canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.grid(row=1, column=0, columnspan=4)
        image_class.canvas = canvas
        image_class.current_image_on_canvas = first_imge_on_canvas

        # Writing column labels ONLY ONCE
        with open(dataset_path, "w", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            keypoints_xy = [key_point + "_" + axis for key_point in user_def_keypoints for axis in AXES]
            writer.writerow(["index", "image_name"] + keypoints_xy)

        config = {
            "image_index": 0,
            "original_images_folder": user_def_images_folder,
            "project_folder_path": project_full_path,
            "dataset_path": dataset_path,
            "image_size": image_class.image_size,
            "key_points_name": user_def_keypoints,
        }

        write_config2db(config)


    else:
        # CONTINUING LAST PROJECT
        intro = False
        data_dict = read_configfdb()

        image_index = data_dict["image_index"]
        original_images_folder = data_dict["original_images_folder"]
        project_folder_path = data_dict["project_folder_path"]
        dataset_path = data_dict["dataset_path"]
        width, height = data_dict["image_size"]
        user_def_keypoints = data_dict["key_points_name"]

        label_counter = LabelCounter(user_def_keypoints)
        label_counter.thresh = True
        user_def_images_folder =  Path(os.path.join(os.getcwd()), Path(original_images_folder.stem))


        filtered = list(filter(images_ext.match, os.listdir(user_def_images_folder)))

        try:
            sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))
        except:
            try:
                sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][2:]))
            except:
                sorted_images = sorted(filtered)


        num_of_images = len(sorted_images)

        image_counter = ImageCounter(num_of_images)
        image_class.image_size = (width, height)
        try:
            current_image_path = os.path.join(user_def_images_folder, sorted_images[image_index])
        except:
            messagebox.showerror(title="Ошибка!", message="Ошибка!", detail="Извините, но прошлый проект не найден")
            return

        for item in main_menu:
            item.destroy()
        for kp in kp_counter.list_of_kps:
            user_def_keypoints.append(kp.cget("text").lower().strip().replace(" ", "_"))
            kp.destroy()

        invis_kp_button = ttk.Button(root, text="Невидимая ключевая точка", width=1000, cursor="hand2", command=lambda:invisible_button(image_class, keypoint_class))
        invis_kp_button.grid(row=2, column=0, columnspan=2, sticky="EWNS")
        label_counter.show_current_label()

        img = ImageTk.PhotoImage(Image.open(current_image_path).convert('RGB').resize((width, height), Image.ANTIALIAS))

        image_class.project_dir_path = project_folder_path

        image_class.image_counter_class = image_counter
        image_class.image_counter_class.current_image = image_index # !!!
        image_class.current_image_path = current_image_path
        image_class.current_image_object = img
        image_class.images_folder_path = user_def_images_folder
        image_class.images_list = sorted_images
        canvas = Canvas(root, width = width, height = height, cursor="hand2", bd=3)
        first_imge_on_canvas = canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.grid(row=1, column=0, columnspan=4)
        image_class.canvas = canvas
        image_class.current_image_on_canvas = first_imge_on_canvas


def create_circle(x, y, r, canvas): #center coordinates, radius

    label_counter.step_up()

    if label_counter.thresh:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        oval = canvas.create_oval(x0, y0, x1, y1, fill="red", outline="black")
        keypoint_stack.update_dict(label_counter.get_current_label_name(), (x, y))
        keypoint_stack.append(oval)

    if not label_counter.show_current_label():
        label_counter.thresh = False
    else:
        label_counter.thresh = True


def key(event):
    pass


@adding_canvas
def callback(event, r, image_class):
    create_circle(event.x, event.y, r, image_class.canvas)


def all_keypoints():
    return [key_point + "_" + axis for key_point in KEY_POINTS for axis in AXES]


class DotPointHolder():
    def __init__():
        pass


class KeyPointsHolder():

    def __init__(self):
        for key_point in all_keypoints():
            setattr(self, key_point, None)

    def load_keypoints_2db(self):
        key_points = self.__dict__


class ImagesHolder():

    def __init__(self):

        self.images_folder_path = None
        self.images_list = None
        self.project_dir_path = None

        self.image_size = None

        self.current_image_index = None
        self.current_image_object = None
        self.current_image_path = None

        self.image_counter_class = None
        self.current_image_on_canvas = None

    def __setattr__(self, name, value):

        if name == "canvas":
            self.__dict__[name] = value
            self.canvas.bind("<Key>", key)
            self.canvas.bind("<Button-1>", callback)
            self.canvas.grid(row=1, column=0, columnspan=3)
        else:
            self.__dict__[name] = value


    def draw_image(self, image_index):
        global user_def_keypoints, end

        self.canvas.destroy()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        canvas = Canvas(root, cursor="hand2", bd=3)

        if self.image_size[0] > screen_width or self.image_size[0]+50 > screen_width:
            width=screen_width-50
        if self.image_size[1] > screen_height or self.image_size[1]+200 > screen_height:
            height=screen_height-200


        try:
            current_image_path = os.path.join(self.images_folder_path, self.images_list[image_index])
            img = ImageTk.PhotoImage(Image.open(current_image_path).convert('RGB').resize((self.image_size[0], self.image_size[1]), Image.ANTIALIAS))
            end = False
            canvas.config(width=self.image_size[0], height=self.image_size[1])

        except Exception as err:
            img = ImageTk.PhotoImage(Image.open(Path(os.path.join("config", "blank.jpg"))))
            end = True
            canvas.config(width=img.width(), height=img.height())

        # canvas.config(width=self.image_size[0], height=self.image_size[1])



        first_imge_on_canvas = canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.grid(row=1, column=0, columnspan=4)

        # Updating info
        if not end:
            self.canvas = canvas
        try:
            self.current_image_on_canvas = first_imge_on_canvas
            self.current_image_path = current_image_path
            self.current_image_object = img
        except:
            answer = messagebox.showinfo(title="Завершение работы", message="Процесс аннотации завершен!")
            sleep(1)
            root.destroy()


root = ThemedTk(theme="equilux")
frame = ttk.Frame(root)
# root = Tk()
root.configure(background=background_color)

kp_counter = KPCounter()
keypoint_stack = KeyPointsSuperStack()
intro = True

root.rowconfigure(list(range(0,31)), weight=1)
root.rowconfigure(0, weight=3)

root.columnconfigure(list(range(0,4)), weight=3)
root.columnconfigure(2, weight=4)
root.columnconfigure(3, weight=4)

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry(f"{screen_width//3}x{screen_height-100}" + "+100+0")

images_holder = ImagesHolder()
key_points_holder = KeyPointsHolder()

images_ext = re.compile(".*(.jpg|.jpeg)")

pattern = re.compile(r'^([\d]*)$')
vcmd = (root.register(validate_numbers), "%i", "%P")

pattern_a = re.compile(r'([a-zA-Z]|\s)*$')
vcmd_a = (root.register(validate_letters), "%i", "%P")


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Выйти", command=on_closing)
menubar.add_cascade(label="Меню", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Инструкция", command=donothing)
menubar.add_cascade(label="Помощь", menu=helpmenu)

root.config(menu=menubar)


main_label = ttk.Label(root, text="Программа для аннотации ключевых точек", width=120, anchor=CENTER)
main_label.grid(row=0, column=0, columnspan=4, sticky="EWNS")


dir_path = StringVar()
project_name = StringVar()
added_title = StringVar()

img_width_var = StringVar()
img_height_var = StringVar()

last_session_var = IntVar()

last_session = ttk.Checkbutton(root, text = "Продолжить последний проект", variable = last_session_var, \
                 onvalue = 1, offvalue = 0, \
                 width = 30, command=disable_entries, cursor="hand2")
last_session.grid(row=1, column=0, columnspan=4, sticky="EWNS")


proj_title = ttk.Label(root, text="Название проекта", width=60, anchor=CENTER)
proj_title.grid(row=2, column=0, columnspan=2, ipadx=100, sticky="EWNS")

proj_entry = ttk.Entry(root, width=60, textvariable=project_name, cursor="hand2")
proj_entry.grid(row=2, column=2, columnspan=2, ipady=7, sticky="EWNS")


img_label_title = ttk.Label(root, text="Разрешение", width=30, anchor=CENTER)
img_label_title.grid(row=4, column=0, columnspan=2, ipadx=100, sticky="EWNS")
img_width_title = ttk.Label(root, text="Ширина", justify=CENTER, width=20, anchor=CENTER)
img_width_title.grid(row=3, column=2, columnspan=1, ipadx=100, sticky="EWNS")
img_height_title = ttk.Label(root, text="Высота", width=20, anchor=CENTER)
img_height_title.grid(row=3, column=3, columnspan=1, ipadx=100, sticky="EWNS")


img_width_entry = ttk.Entry(root, width=20, textvariable=img_width_var, validate="key", validatecommand=vcmd, cursor="hand2")
img_width_entry.grid(row=4, column=2, columnspan=1, ipady=8, sticky="EWNS")
img_height_entry = ttk.Entry(root, width=20, textvariable=img_height_var, validate="key", validatecommand=vcmd, cursor="hand2")
img_height_entry.grid(row=4, column=3, columnspan=1, ipady=8, sticky="EWNS")


dir_entry = ttk.Entry(root, width=60, textvariable=dir_path, cursor="hand2")
dir_entry.grid(row=5, column=2, columnspan=2, padx=5, pady=10, ipady=9, sticky="EWNS")

select_button = ttk.Button(root, text="Путь к папке", command=dirinput, width=60, cursor="hand2")
select_button.grid(row=5, column=0, columnspan=2, sticky="EWNS")


kp_label_title = ttk.Label(root, text="Добавление ключевых точек", width=120, anchor=CENTER)
kp_label_title.grid(row=6, column=0, columnspan=4, ipadx=100, sticky="EWNS")

add_entry = ttk.Entry(root, width=120, textvariable=added_title, validate="key", validatecommand=vcmd_a, cursor="hand2")
add_entry.grid(row=7, column=0, columnspan=4, ipady=5, sticky="EWNS")


start_button = ttk.Button(root, text="Начать", command=lambda:start_annotation(dir_path.get(), images_holder, key_points_holder), width=60, cursor="hand2")
start_button.grid(row=30, column=0, columnspan=4, sticky="EWNS")


root.bind('<Control-n>', next_imageKeyPress)
root.bind('<Control-z>', undo_keypoint)
root.bind('<Return>', add_keypoint)

root.protocol("WM_DELETE_WINDOW", on_closing)

main_menu = [
    main_label, img_label_title, img_height_title,
    img_width_title, img_height_entry, img_width_entry,
    dir_entry, select_button, start_button,
    add_entry, kp_label_title, last_session, proj_entry, proj_title,
]


root.mainloop()
