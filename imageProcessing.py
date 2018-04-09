import cv2 as cv

class ImageProcessing:

    def __init__(self):
        pass

    def CropImage(image, x1, x2, y1, y2):
        return image[x1:x2, y1:y2]

    def GaussianBlur(image):
        blurFilter = cv.GaussianBlur(image,(5,5),0)

    def Threshold(image, level):
        cv.threshold(image, level, 255, 1)
