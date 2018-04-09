from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv

imgGol1 = cv.imread("C:/Users/oluis/Desktop/TCC/tutorias/plate_recognition/plates/gol1.jpg", cv.IMREAD_GRAYSCALE)

img = Frame(imgGol1, 'gol', None)

ImageProcessing.Threshold(img.image, 100)

img.show()

cv.waitKey(0)