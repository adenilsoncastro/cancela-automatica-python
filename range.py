import cv2
import numpy as np

## Read
img = cv2.imread("../../images/siena1.jpg")

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

## mask of green (36,0,0) ~ (70, 255,255)
# mask = cv2.inRange(hsv, (0, 0, 0), (180, 180,240))
mask = cv2.inRange(hsv, (0, 0, 0), (70, 70,250))

## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

## save 
cv2.imshow("green.png", green)
cv2.waitKey(0)