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
            # cv.imwrite(self.name + str(i) + '.png', plate.image)
            print(self.name + ": " + str(i) + str(plate.shape()))

    
    def showAllPlatesThreshold(self):
        i = 0
        for plate in self.arrayOfPlates:
            i = i + 1
            _, plate.image = cv.threshold(plate.image, 105, 255, 0)
            cv.imshow(self.name + "_threshold: " + str(i), plate.image)
            cv.imwrite(self.name + str(i) + '_threshold.png', plate.image)
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
        y, x = plate.image.shape

        y1New = int(np.ceil(y - y * 0.15))
        x1New = int(np.ceil(x - x * 0.05))

        y2New = int(np.ceil(y * 0.31))
        x2New = int(np.ceil(x * 0.05))
        
        plate.image = plate.image[y2New:y1New, x2New:x1New]
        return plate

    def CropAllPlatesBorders(self):
        for plate in self.arrayOfPlates:
           plate = self.CropPlateBorders(plate)

