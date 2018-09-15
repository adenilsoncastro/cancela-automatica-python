from frame import Frame
from imageProcessing import ImageProcessing
import cv2 as cv
import numpy as np
imgPlaca = cv.imread("C:/Users/oluis/Desktop/images/original/torta.png", cv.IMREAD_GRAYSCALE)

plateCopy = imgPlaca.copy()

imgProcessing = ImageProcessing()

plateCopy = imgProcessing.MoreLight(plateCopy)
plateCopy = imgProcessing.Billateral(plateCopy)
plateCopy = imgProcessing.Canny(plateCopy)
    
findContournsImg, contoursPlate, hierarchy = cv.findContours(plateCopy.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
backtorgbplate = cv.cvtColor(plateCopy, cv.COLOR_GRAY2RGB)

for contour in contoursPlate:
    x,y,w,h = cv.boundingRect(contour)
    proportion = float(w) / h
    if proportion > 0.57 and proportion < 0.84 and h > 11:
        cv.rectangle(backtorgbplate,(x,y),(x+w,y+h),(0,0,255),1)
                
cv.imshow('placa', backtorgbplate)

cv.waitKey(0)