from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np
imgGol1 = cv.imread("D:/rejected/pixelcolor/ostu3cd3349e.png7328de2b-bfaa-497b-b545-bf3c0f869472.png", cv.IMREAD_GRAYSCALE)
# imgGol2 = cv.imread("D:/rejected/pixelcolor/22dc8137.png950955d2-01b4-49ca-af82-ce05e69aa72a.png", cv.IMREAD_GRAYSCALE)
# imgGol3 = cv.imread("D:/rejected/pixelcolor/1b89397b.png2c313f7f-cc9c-45b4-81f4-22a26db455f9.png", cv.IMREAD_GRAYSCALE)

arrayOfCarsInitial = np.array([imgGol1])

i = 0

for car in arrayOfCarsInitial:
    i = i + 1
    img = Frame(car, 'car' + str(i), None, None)
    img.showAmountOfColor(car)
    print(' ')