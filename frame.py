import cv2 as cv
import numpy as np

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
            print(self.name + ": " + str(i) + str(plate.shape()))

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
        x1, y1 = plate.image.shape
        x1New = int(np.ceil(x1 - x1 * 0.1))
        y1New = int(np.ceil(y1 - y1 * 0.1))
        plate.image = plate.image[0:x1New, 0:y1New]
        return plate

    def CropAllPlatesBorders(self):
        for plate in self.arrayOfPlates:
           plate = self.CropPlateBorders(plate)

