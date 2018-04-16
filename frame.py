import cv2 as cv

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
            cv.imshow(self.name + ": " + str(i), plate)

    def CropImage(self, x1, x2, y1, y2):
        self.originalImage = self.originalImage[x1:x2, y1:y2]
        self.image = self.image[x1:x2, y1:y2]