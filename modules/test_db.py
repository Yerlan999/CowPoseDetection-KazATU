import pickle, csv, os
from pathlib import Path
# from tools import AXES
# import numpy as np

# # config = {
# #     "image_index": 0,
# #     "original_images_folder": "",
# #     "project_folder_path": "",
# #     "dataset_path": "",
# # }

# def write_config2db(dict_of_data):

#     pickle_out = open(Path(os.path.join("config", "db.pickle")),"wb")
#     pickle.dump(dict_of_data, pickle_out)
#     pickle_out.close()


def read_configfdb():

    pickle_in = open(Path(os.path.join("config", "db.pickle")),"rb")
    return pickle.load(pickle_in)




# contin_last_session = last_session_var.get()


# if not contin_last_session:

#     # STARTING NEW PROJECT

#     user_def_images_folder = Path(dirname)
#     # user_def_keypoints = ["left_ear", "right_ear", "left_eye", "right_eye"]
#     # project_name = proj_entry.get()
#     project_full_path = Path(os.path.join(os.getcwd(), project_name))

#     if not os.path.isdir(project_name):
#         os.mkdir(project_name)
#         os.chdir(project_name)
#         os.mkdir("gray_images")
#         os.mkdir("colored_images")
#         os.chdir("..")

#     dataset_path = Path(os.path.join(project_name, f"{project_name}_dataset.csv"))

#     # Writing column labels ONLY ONCE
#     with open(dataset_path, "w", newline='') as file:
#         writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         keypoints_xy = [key_point + "_" + axis for key_point in user_def_keypoints for axis in AXES]
#         writer.writerow(["index", "image_name"] + keypoints_xy)

#     config = {
#     "image_index": 0,
#     "original_images_folder": user_def_images_folder,
#     "project_folder_path": project_name,
#     "dataset_path": Path(os.path.join(project_name, f"{project_name}_dataset.csv")),
#     "image_size": (width, height),
#     "key_points_name": user_def_keypoints,
#     }

#     write_config2db(config)

#     print("New Session is created!")

# else:

#     # CONTINUING LAST PROJECT

data_dict = read_configfdb()

#     image_index = data_dict["image_index"]
#     original_images_folder = data_dict["original_images_folder"]
#     project_folder_path = data_dict["project_folder_path"]
#     dataset_path = data_dict["dataset_path"]
#     width, height = data_dict["image_size"]
#     user_def_keypoints = data_dict["key_points_name"]


#     print("Last Session is loaded!")
print(data_dict)
