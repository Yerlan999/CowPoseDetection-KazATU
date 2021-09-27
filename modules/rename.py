import os, sys, uuid
from datetime import datetime


print("STARTED!!!")

num_of_pics = len([file for file in os.listdir() if file.endswith(".jpg") or file.endswith(".jpeg")])

print(num_of_pics)


for i, file in enumerate(os.listdir()):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        random_name = '{}{:-%Y%m%d%H%M%S}.jpeg'.format(str(uuid.uuid4().hex), datetime.now())
        os.rename(file, random_name + ".jpg")


for i, file in enumerate(os.listdir()):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        os.rename(file, "cow" + str(i) + ".jpg")


print("FINISHED!!")
