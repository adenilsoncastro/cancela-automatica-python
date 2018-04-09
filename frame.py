import cv2 as cv

class Frame:
    def __init__(self, image, name, time):
        self.image = image
        self.name = name
        self.time = time

    def show(self):
        cv.imshow(self.name, self.image)
    
    def shape(self):
        height, width = self.image.shape
        print('height: ' + str(height))
        print('width: ' + str(width))