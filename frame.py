import cv2 as cv
import numpy as np
from PIL import Image
import os
#from matplotlib import pyplot as plt
import uuid

class Frame:
    def __init__(self, image, name, time, arrayOfPlates):
        self.image = image
        self.originalImage = image.copy()
        self.name = name
        self.time = time
        self.arrayOfPlates = arrayOfPlates
        self._id = str(uuid.uuid4()).split('-')[0]

    def showAmountOfColor(self, image):
        white = black = 0
        lower = 255/3
        upper = 2*lower
        height, width = image.shape
  
        for i in range(height):
            for j in range(width):
                if image[i,j] > upper:
                    white += 1                        
                else:
                    black += 1
  
        all = width*height

        whiteR = 100.0*white/all
        blackR = 100.0*black/all

        print ("White pixels: %d (%5.2f%%)" % (white, whiteR))
        print ("Black pixels: %d (%5.2f%%)" % (black, blackR))

        return whiteR,blackR

    def show(self):
        cv.imshow(self.name, self.image)

    def shape(self):
        height, width = self.image.shape
        print('height: ' + str(height))
        print('width: ' + str(width))

    def showAllPlates(self):
        i = 0
        for plate in self.arrayOfPlates:
            i = i + 1
            cv.imshow(self.name + ": " + str(i), plate.image)
            # cv.imwrite(self.name + str(i) + '.png', plate.image)
            print(self.name + ": " + str(i) + str(plate.shape()))

    def showAllPlatesThreshold(self):
        print(" ")
        i = 0
        for plate in self.arrayOfPlates:
            i = i + 1
            
            # cv.imwrite(self.name + str(i) + 'clean.png', plate.image)
            adaptive = cv.adaptiveThreshold(plate.image.copy(),255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,7,2)
            ret, otsu = cv.threshold(plate.image.copy(),0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
            _, plate.image = cv.threshold(plate.image, 105, 255, 0)

            cv.imshow(self.name + "_threshold: " + str(i), plate.image)
            cv.imshow(self.name + "_thresholdAdaptive: " + str(i), adaptive)
            cv.imshow(self.name + "_thresholdOtsu: " + str(i), otsu)
            
            # cv.imwrite(self.name + str(i) + '_threshold.png', plate.image)
            print(self.name + ": " + str(i) + str(plate.shape()))

            # histThresh = cv.calcHist([plate.image],[0],None,[256],[0,256])
            # histOtsu = cv.calcHist([otsu],[0],None,[256],[0,256])
            # plt.plot(histThresh)
            # plt.plot(histOtsu)
            # plt.show()
                
    def validateAmountOfWhiteAndBlackPixels(self):
        print(" ")
        i = 0
        for plate in self.arrayOfPlates:
            i = i + 1
            
            # adaptive = cv.adaptiveThreshold(plate.image.copy(),255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,2)
            ret, otsu = cv.threshold(plate.image.copy(),0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
            # aret, teste = cv.threshold(plate.image.copy(),150,255,0)
            _, normal = cv.threshold(plate.image.copy(), 105, 255, 0)

            # cv.imshow('adaptive', adaptive)
            # cv.imshow('otsu', otsu)
            # cv.imshow('normal', plate.name)

            print('normal')
            white_normal, black_normal = self.showAmountOfColor(normal)

            # print('adaptive')
            # white_adaptive, black_adaptive = self.showAmountOfColor(adaptive)

            # print('otsu')
            # white_otsu, black_otsu = self.showAmountOfColor(otsu)

            if white_normal < 20:
                _, teste = cv.threshold(plate.image.copy(), 55, 255, cv.THRESH_BINARY)
                cv.imshow(self.name + "_newThreshold_applied: " + str(i), teste)
                return

            if white_normal > 70 :
                cv.imshow(self.name + "normal: " + str(i), plate.image)
                ret, plate.image = cv.threshold(plate.image.copy(),0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
                print('otsu applied: ' + plate.name)
                cv.imshow(self.name + "_otsu_applied: " + str(i), plate.image)
                return
                # if white_otsu < 50 :
                #     self.arrayOfPlates.pop(i - 1)
                #     print("removed: " + plate.name)
                #     cv.imwrite("../rejected/pixelcolor/ostu" + self.name + str(uuid.uuid4()) + '.png', plate.image)
            
            plate.image = normal
            cv.imshow(self.name + "normal: " + str(i), plate.image)

    def showShapeOfPlates(self):
        i = 0
        print('plate shape: ' + self.name)
        for plate in self.arrayOfPlates:
            i = i + 1
            cv.imshow(self.name + ": " + str(i), plate)

    def CropImage(self, x1, x2, y1, y2):
        self.originalImage = self.originalImage[x1:x2, y1:y2]
        self.image = self.image[x1:x2, y1:y2]

    def CropPlateBorders(self, plate):
        y, x = plate.image.shape

        y1New = int(np.ceil(y - y * 0.05))
        x1New = int(np.ceil(x - x * 0.05))

        y2New = int(np.ceil(y * 0.31))
        x2New = int(np.ceil(x * 0.05))

        plate.image = plate.image[y2New:y1New, x2New:x1New]
        return plate

    def CropAllPlatesBorders(self):
        for plate in self.arrayOfPlates:
           plate = self.CropPlateBorders(plate)

    def SaveImage(self):
        cv.imwrite(os.path.join("../../", self.name), self.image)        
        for plate in self.arrayOfPlates:
            cv.imwrite(os.path.join("../../", self.name + '_result.jpg'), plate.image)

