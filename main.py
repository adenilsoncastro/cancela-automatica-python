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
imgGol11 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol11.jpg", cv.IMREAD_GRAYSCALE)
imgGol12 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol12.jpg", cv.IMREAD_GRAYSCALE)
imgGol13 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol13.jpg", cv.IMREAD_GRAYSCALE)
imgGol14 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol14.jpg", cv.IMREAD_GRAYSCALE)
imgGol15 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol15.jpg", cv.IMREAD_GRAYSCALE)
imgGol16 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol16.jpg", cv.IMREAD_GRAYSCALE)
imgGol17 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol17.jpg", cv.IMREAD_GRAYSCALE)
imgGol18 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol18.jpg", cv.IMREAD_GRAYSCALE)

# arrayOfCarsInitial = np.array([imgGol1, imgGol2, imgGol3, imgGol4, imgGol5, imgGol6, imgGol7, imgGol8, imgGol9, imgGol10])
arrayOfCarsInitial = np.array([imgGol4, imgGol7, imgGol9, imgGol10, imgGol11, imgGol12, imgGol13, imgGol14, imgGol15])

cap = cv.VideoCapture('C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol_video.mp4')

i = 0

# img = Frame(imgGol1, 'gol', None, None)

# imgProcessing = ImageProcessing()

# img.CropImage(500, 1500, 400, 1500)
# img.image = imgProcessing.GaussianBlur(img.image)
# img.image = imgProcessing.Canny(img.image)
# imgProcessing.FindPossiblePlates(img)
# img.showAllPlates()

# for car in arrayOfCarsInitial:
#     i = i + 1
#     img = Frame(car, 'gol' + str(i), None, None)

#     imgProcessing = ImageProcessing()

#     img.CropImage(500, 1500, 400, 1500)
#     # img.image = imgProcessing.GaussianBlur(img.image)
#     img.image = imgProcessing.Billateral(img.image)
#     img.image = imgProcessing.Canny(img.image)
#     imgProcessing.FindPossiblePlates(img)

while(cap.isOpened()):
    ret, frame = cap.read()
    i = i + 1
    if i % 100 == 0:
        if frame is not None:
            img = Frame(frame, 'gol' + str(i), None, None)

            imgProcessing = ImageProcessing()

            img.CropImage(500, 1500, 400, 1500)
            # img.image = imgProcessing.GaussianBlur(img.image)
            img.image = imgProcessing.Billateral(img.image)
            img.image = imgProcessing.Canny(img.image)
            imgProcessing.FindPossiblePlates(img)
        if i == 400:
            cap.release()

cap.release()

cv.waitKey(0)