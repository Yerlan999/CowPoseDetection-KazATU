LABELS = [
    "L_eye_x",
    "L_eye_y",
    "R_eye_x",
    "R_eye_y",
    "L_ear_x",
    "L_ear_y",
    "R_ear_x",
    "R_ear_y",
    "Nose_x",
    "Nose_y",
    "Throat_x",
    "Throat_y",
    "Tail_x",
    "Tail_y",
    "withers_x",
    "withers_y",
    "L_F_elbow_x",
    "L_F_elbow_y",
    "R_F_elbow_x",
    "R_F_elbow_y",
    "L_B_elbow_x",
    "L_B_elbow_y",
    "R_B_elbow_x",
    "R_B_elbow_y",
    "L_F_knee_x",
    "L_F_knee_y",
    "R_F_knee_x",
    "R_F_knee_y",
    "L_B_knee_x",
    "L_B_knee_y",
    "R_B_knee_x",
    "R_B_knee_y",
    "L_F_paw_x",
    "L_F_paw_y",
    "R_F_paw_x",
    "R_F_paw_y",
    "L_B_paw_x",
    "L_B_paw_y",
    "R_B_paw_x",
    "R_B_paw_y"
]

SHAPE = (300, 200)


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


def all_keypoints():
    return [key_point + "_" + axis for key_point in KEY_POINTS for axis in AXES]

