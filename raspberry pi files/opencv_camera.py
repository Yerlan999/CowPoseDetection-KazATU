#!/usr/bin/python3

import cv2

# from null_preview import *
from picamera2 import *

# Grab images as numpy arrays and leave everything else to OpenCV.

# face_detector = cv2.CascadeClassifier("/usr/local/lib/python3.9/dist-packages/cv2/data/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
# preview = NullPreview(picam2)
picam2.configure(picam2.preview_configuration(main={"size": (640, 480)}))
picam2.start()

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # faces = face_detector.detectMultiScale(grey, 1.1, 5)

    # for (x, y, w, h) in faces:
    #     cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Camera", im)


#                   1 2 3      0 1
# xy_predictions[point index][x or y]

dist_coef = abs(xy_predictions[1][0] - xy_predictions[3][0])/300 # 0 - 1 close - far


(xy_predictions[2][1] < xy_predictions[1][1]) and (xy_predictions[2][1] < xy_predictions[3][1]):
