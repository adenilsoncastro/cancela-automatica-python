import cv2 as cv
import numpy as np
from PIL import Image

class Frame:
    def __init__(self, image, name, time, arrayOfPlates):
        self.image = image
        self.originalImage = image.copy()
        self.name = name
        self.time = time
        self.arrayOfPlates = arrayOfPlates

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
        i = 0
        for plate in self.arrayOfPlates:
            i = i + 1
            th3 = cv.adaptiveThreshold(plate.image.copy(),255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,7,2)
            ret, otsu = cv.threshold(plate.image.copy(),0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
            cv.imwrite(self.name + str(i) + 'clean.png', plate.image)
            _, plate.image = cv.threshold(plate.image, 105, 255, 0)
            cv.imshow(self.name + "_threshold: " + str(i), plate.image)
            cv.imshow(self.name + "_thresholdAdaptive: " + str(i), th3)
            cv.imshow(self.name + "_thresholdOtsu: " + str(i), otsu)
            # cv.imwrite(self.name + str(i) + '_threshold.png', plate.image)
            print(self.name + ": " + str(i) + str(plate.shape()))
            # im = Image.fromarray(np.uint8(plate.image))
            # print(im.info['dpi'])

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

        y1New = int(np.ceil(y - y * 0.12))
        x1New = int(np.ceil(x - x * 0.05))

        y2New = int(np.ceil(y * 0.31))
        x2New = int(np.ceil(x * 0.05))

        plate.image = plate.image[y2New:y1New, x2New:x1New]
        return plate

    def CropAllPlatesBorders(self):
        for plate in self.arrayOfPlates:
           plate = self.CropPlateBorders(plate)