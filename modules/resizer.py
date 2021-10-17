import cv2, os, csv, re, shutil
import pandas as pd


def pairwise_2(iterable):
    a = iter(iterable)
    return zip(a, a)

print("Started resizing...")

old_size = (300, 200)
new_size = (200, 100)
csv_file_path = r"Training_Project_dataset.csv"
cimages_dirname = r"colored"
gimages_dirname = r"grayscaled"
keypoints_df = pd.read_csv(csv_file_path)
resized_keypoints_df = keypoints_df.copy()

images_ext = re.compile(".*(.jpg|.jpeg)")
filtered = list(filter(images_ext.match, os.listdir(cimages_dirname)))
sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))

if os.path.isdir("resized"):
    shutil.rmtree('resized')
    os.mkdir("resized")
    os.chdir("resized")
    os.mkdir("colored");os.mkdir("grayscaled")
    os.chdir("..")
else:
    os.mkdir("resized")
    os.chdir("resized")
    os.mkdir("colored");os.mkdir("grayscaled")
    os.chdir("..")

for image in sorted_images:
    cimage = cv2.imread(os.path.join(cimages_dirname, image))
    resized_cimage = cv2.resize(cimage, new_size, interpolation = cv2.INTER_AREA)
    cv2.imwrite(os.path.join("resized\\colored\\", image), resized_cimage)


filtered = list(filter(images_ext.match, os.listdir(gimages_dirname)))
sorted_images = sorted(filtered ,key=lambda x: int(os.path.splitext(x)[0][3:]))
for image in sorted_images:
    gimage = cv2.imread(os.path.join(gimages_dirname, image))
    resized_gimage = cv2.resize(gimage, new_size, interpolation = cv2.INTER_AREA)
    cv2.imwrite(os.path.join("resized\\grayscaled\\", image), resized_gimage)



for row in range(len(keypoints_df.index)):
    for pair in pairwise_2(range(len(keypoints_df.columns[2:]))):
        old_x = keypoints_df.iloc[row,2:][pair[0]]
        old_y = keypoints_df.iloc[row,2:][pair[1]]
        new_x = old_x//(old_size[0]/new_size[0])
        new_y = old_y//(old_size[1]/new_size[1])
        resized_keypoints_df.iat[row,pair[0]+2] = new_x
        resized_keypoints_df.iat[row,pair[1]+2] = new_y

with open(csv_file_path, "w", newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(list(keypoints_df.columns))
with open(csv_file_path, "a", newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in resized_keypoints_df.values.tolist():
        writer.writerow(row)

print("Finished resizing!")
