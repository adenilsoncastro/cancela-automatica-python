from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np
from camera import Camera
import queue
from ocr import OcrThread

imgGol1 = cv.imread("../../images/gol1.jpg", cv.IMREAD_GRAYSCALE)
imgGol2 = cv.imread("../../images/gol2.jpg", cv.IMREAD_GRAYSCALE)
imgGol3 = cv.imread("../../images/gol3.jpg", cv.IMREAD_GRAYSCALE)
imgGol4 = cv.imread("../../images/gol4.jpg", cv.IMREAD_GRAYSCALE)
imgGol5 = cv.imread("../../images/gol5.jpg", cv.IMREAD_GRAYSCALE)
imgGol6 = cv.imread("../../images/gol6.jpg", cv.IMREAD_GRAYSCALE)
imgGol7 = cv.imread("../../images/gol7.jpg", cv.IMREAD_GRAYSCALE)
imgGol8 = cv.imread("../../images/gol8.jpg", cv.IMREAD_GRAYSCALE)
imgGol9 = cv.imread("../../images/gol9.jpg", cv.IMREAD_GRAYSCALE)
imgGol10 = cv.imread("../../images/gol10.jpg", cv.IMREAD_GRAYSCALE)
imgGol11 = cv.imread("../../images/gol11.jpg", cv.IMREAD_GRAYSCALE)
imgGol12 = cv.imread("../../images/gol12.jpg", cv.IMREAD_GRAYSCALE)
imgGol13 = cv.imread("../../images/gol13.jpg", cv.IMREAD_GRAYSCALE)
imgGol14 = cv.imread("../../images/gol14.jpg", cv.IMREAD_GRAYSCALE)
imgGol15 = cv.imread("../../images/gol15.jpg", cv.IMREAD_GRAYSCALE)
imgGol16 = cv.imread("../../images/gol16.jpg", cv.IMREAD_GRAYSCALE)
imgGol17 = cv.imread("../../images/ol17.jpg", cv.IMREAD_GRAYSCALE)
imgGol18 = cv.imread("../../images/gol18.jpg", cv.IMREAD_GRAYSCALE)

# arrayOfCarsInitial = np.array([imgGol1, imgGol2, imgGol3, imgGol4, imgGol5, imgGol6, imgGol7, imgGol8, imgGol9, imgGol10])
arrayOfCarsInitial = np.array([imgGol4, imgGol7, imgGol9, imgGol10, imgGol11, imgGol12, imgGol13, imgGol14, imgGol15])

cap = cv.VideoCapture('../../images/gol_video.mp4')


#cam = Camera()
#cam.capture("640x720", "test", "jpg")
#
#result_ocr = queue.Queue()
#ocr = OcrThread()
#ocr.create_ocr_thread(imgGol1, result_ocr)

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