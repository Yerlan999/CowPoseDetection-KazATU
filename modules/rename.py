import os, sys

print("STARTED!!!")

num_of_pics = len([file for file in os.listdir() if file.endswith(".jpg") or file.endswith(".jpeg")])

print(num_of_pics)


for i, file in enumerate(os.listdir()):
    if file.endswith(".jpg") or file.endswith(".jpeg"):
        os.rename(file, "cow" + str(i) + ".jpg")

print("FINISHED!!")
