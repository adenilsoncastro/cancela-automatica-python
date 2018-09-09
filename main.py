from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np
from camera import Camera
import queue
from ocr import OcrThread
# import platews

# response = platews.checkForPlateExistence('ayh-2598')

# exit()

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

sandero1 = cv.imread("../../images/sandero-1.jpg", cv.IMREAD_GRAYSCALE)
sandero2 = cv.imread("../../images/sandero-2.jpg", cv.IMREAD_GRAYSCALE)
sandero3 = cv.imread("../../images/sandero-3.jpg", cv.IMREAD_GRAYSCALE)
sandero4 = cv.imread("../../images/sandero-4.jpg", cv.IMREAD_GRAYSCALE)
corsa1 = cv.imread("../../images/corsa-1.jpg", cv.IMREAD_GRAYSCALE)
corsa2 = cv.imread("../../images/corsa-2.jpg", cv.IMREAD_GRAYSCALE)
siena1 = cv.imread("../../images/siena1.jpg", cv.IMREAD_GRAYSCALE)
meriva1 = cv.imread("../../images/meriva1.jpg", cv.IMREAD_GRAYSCALE)
peugeot1 = cv.imread("../../images/peugeot1.jpg", cv.IMREAD_GRAYSCALE)
hb201 = cv.imread("../../images/hb201.jpg", cv.IMREAD_GRAYSCALE)

noite1 = cv.imread("../../images/noite1.png", cv.IMREAD_GRAYSCALE)
noite2 = cv.imread("../../images/noite2.png", cv.IMREAD_GRAYSCALE)
noite3 = cv.imread("../../images/noite3.png", cv.IMREAD_GRAYSCALE)
noite4 = cv.imread("../../images/noite4.png", cv.IMREAD_GRAYSCALE)
noite5 = cv.imread("../../images/noite5.png", cv.IMREAD_GRAYSCALE)
noite6 = cv.imread("../../images/noite6.png", cv.IMREAD_GRAYSCALE)
noite7 = cv.imread("../../images/noite7.png", cv.IMREAD_GRAYSCALE)
noite8 = cv.imread("../../images/noite8.png", cv.IMREAD_GRAYSCALE)

# arrayOfCarsInitial = np.array([imgGol1, imgGol2, imgGol3, imgGol4, imgGol5, imgGol6, imgGol7, imgGol8, imgGol9, imgGol10])
# arrayOfCarsInitial = np.array([imgGol2, imgGol3, imgGol4, imgGol5, imgGol7, imgGol9, imgGol10, imgGol11, imgGol12, imgGol13, imgGol14, imgGol15])
# arrayOfCarsInitial = np.array([imgGol11,sandero1,sandero2, sandero3,sandero4,corsa1,corsa2,siena1, meriva1, peugeot1, hb201, imgGol14])
# arrayOfCarsInitial = np.array([imgGol11,sandero1,sandero2, sandero3,sandero4])
arrayOfCarsInitial = np.array([meriva1, corsa1,corsa2])
arrayOfCarsInitial = np.array([corsa1])
# arrayOfCarsInitial = np.array([noite1, noite2, noite3, noite4, noite5, noite6])
# arrayOfCarsInitial = np.array([noite1, noite8])

i = 0

for car in arrayOfCarsInitial:
    i = i + 1
    img = Frame(car, 'car' + str(i), None, None)

    imgProcessing = ImageProcessing()

    img.CropImage()
    cv.imshow('inicial crop' + img.name, img.image)
    img.image = imgProcessing.Billateral(img.image)
    img.image = imgProcessing.Canny(img.image)

    imgProcessing.FindPossiblePlates(img, False)

    if(len(img.arrayOfPlates) == 0):
        print('no plates found in ' + img.name)
        print('applying dilate filter')
        dilate = imgProcessing.Dilate(img.image)
        img.image = dilate
        imgProcessing.FindPossiblePlates(img, False)
        if(len(img.arrayOfPlates) == 0):
            print('no plates found after dilate in ' + img.name)
            print('applying gaussian blur filter')
            img.image = imgProcessing.GaussianBlur(img.image)
            imgProcessing.FindPossiblePlates(img, False)

    if(len(img.arrayOfPlates) == 0):
        print('no plates found after gaussian in ' + img.name)
        print('applying bright filter')
        img.image = imgProcessing.MoreLight(img.originalImage)
        cv.imshow('light ' + img.name, img.image)
        img.image = imgProcessing.Billateral(img.image)
        img.image = imgProcessing.Canny(img.image)
        imgProcessing.FindPossiblePlates(img, True)
        if(len(img.arrayOfPlates) == 0):
            print('no plates found in ' + img.name)
            print('applying dilate filter')
            dilate = imgProcessing.Dilate(img.image)
            img.image = dilate
            imgProcessing.FindPossiblePlates(img, False)
            if(len(img.arrayOfPlates) == 0):
                print('no plates found after dilate in ' + img.name)
                print('applying gaussian blur filter')
                img.image = imgProcessing.GaussianBlur(img.image)
                imgProcessing.FindPossiblePlates(img, False)

    img.CropAllPlatesBorders()
    img.validateAmountOfWhiteAndBlackPixels()

cv.waitKey(0)