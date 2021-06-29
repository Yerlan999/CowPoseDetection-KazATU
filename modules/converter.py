import numpy as np
import os, csv, re
from tkinter import *
from PIL import Image
from pathlib import Path
from tkinter import Tk, Label, Button, IntVar, messagebox
from tkinter.ttk import Progressbar



class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('300x300+330+80')
        label = Label(self, text="Конвертация")
        label.grid(row=2, column=0, columnspan=3, sticky="EWNS")

        # NEW Add to keep track of the progress bar value
        self.value = IntVar()
        self.value.set(0)
        ######

        # Modified this line to add the variable parameter
        self.progress_bar = Progressbar(self, orient="horizontal", length = 200, mode="determinate", variable=self.value)
        ##########
        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky="EWNS")

        # Modified to add the command parameter
        stop_button = Button(self, text='Остановить', command=self.stop_progress_bar)
        start_button = Button(self, text='Начать', command=self.start_progress_bar)

        start_button.grid(row=5,column=0, sticky="EWNS")
        stop_button.grid(row=5,column=2, sticky="EWNS")

    # NEW: Added these functions to update the progress bar
    def stop_progress_bar(self):
        self.progress_bar.stop()

    def start_progress_bar(self):

        # IMAGE TO STRING CONVERTION
        images_list = []
        for image in sorted_images:

            an_image = Image.open(image)
            image_sequence = an_image.getdata()
            image_array = np.array(image_sequence)

            image_as_str = ''
            for pix in image_array:
                image_as_str += (str(pix) + " ")
            images_list.append((image, image_as_str.strip()))

            self.increment(200/len(sorted_images))
            self.update_idletasks()


        with open("images_dataset.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["index", "name", "image"])
            for index, tup in enumerate(images_list):
                name, image_str = tup
                writer.writerow([index, name, image_str])

        if self.value.get() == 200:
            answer = messagebox.showinfo(title="Конвертация", message="Конвертация завершена!")
            self.destroy()


    def increment(self, inc):
        self.value.set(self.value.get()+inc)


images_ext = re.compile(".*(.jpg|.jpeg)")

filtered = list(filter(images_ext.match, os.listdir(os.getcwd())))

try:
    sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))
except:
    try:
        sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][2:]))
    except:
        sorted_images = sorted(filtered)


app = App()

app.rowconfigure(list(range(0,10)), weight=1)
app.columnconfigure(list(range(0,3)), weight=1)

app.mainloop()
