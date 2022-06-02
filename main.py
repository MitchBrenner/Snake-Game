import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

# detection with detection confidence of 0.8 instead of .5
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)


    if hands:
        # This is a dictionary and we are accessing lmList
        landmark_list = hands[0]['lmList']
        # element at 8 will give us xyz, and we do not need z so just get x, y by using range
        pointIndex = landmark_list[8][0:2]
        cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)

    cv2.imshow("Snake Game", img)
    cv2.waitKey(1)
