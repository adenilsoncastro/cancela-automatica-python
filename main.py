from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np

imgGol1 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol1.jpg", cv.IMREAD_GRAYSCALE)
imgGol2 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol2.jpg", cv.IMREAD_GRAYSCALE)
imgGol3 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol3.jpg", cv.IMREAD_GRAYSCALE)
imgGol4 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol4.jpg", cv.IMREAD_GRAYSCALE)
imgGol5 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol5.jpg", cv.IMREAD_GRAYSCALE)
imgGol6 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol6.jpg", cv.IMREAD_GRAYSCALE)
imgGol7 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol7.jpg", cv.IMREAD_GRAYSCALE)
imgGol8 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol8.jpg", cv.IMREAD_GRAYSCALE)
imgGol9 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol9.jpg", cv.IMREAD_GRAYSCALE)
imgGol10 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol10.jpg", cv.IMREAD_GRAYSCALE)

# arrayOfCarsInitial = np.array([imgGol1, imgGol2, imgGol3, imgGol4, imgGol5, imgGol6, imgGol7, imgGol8, imgGol9, imgGol10])
arrayOfCarsInitial = np.array([imgGol1, imgGol2, imgGol10])

i = 0

# img = Frame(imgGol1, 'gol', None, None)

# imgProcessing = ImageProcessing()

# img.CropImage(500, 1500, 400, 1500)
# img.image = imgProcessing.GaussianBlur(img.image)
# img.image = imgProcessing.Canny(img.image)
# imgProcessing.FindPossiblePlates(img)
# img.showAllPlates()

for car in arrayOfCarsInitial:
    i = i + 1
    img = Frame(car, 'gol' + str(i), None, None)

    imgProcessing = ImageProcessing()

    img.CropImage(500, 1500, 400, 1500)
    img.image = imgProcessing.GaussianBlur(img.image)
    img.image = imgProcessing.Canny(img.image)
    imgProcessing.FindPossiblePlates(img)

cv.waitKey(0)