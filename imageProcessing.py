import cv2 as cv
import numpy as np

class ImageProcessing:

    def __init__(self):
        pass

    def GaussianBlur(self, image):
        return cv.GaussianBlur(image,(5,5),0)

    def Canny(self, image):
        return cv.Canny(image, 135, 255)

    def Threshold(self, image, level):
        return cv.threshold(image, level, 255, 1)

    def FindPossiblePlates(self, frame):

        cv.imshow('inicial ' + frame.name, frame.image)
        arrayOfPlates = []

        # procura os contornos
        findContournsImg, contours, hierarchy = cv.findContours(frame.image.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # converte a imagem pra colorida apenas para a melhor visualziação
        backtorgb = cv.cvtColor(findContournsImg, cv.COLOR_GRAY2RGB)

        hierarchy = hierarchy[-1] # get the actual inner list of hierarchy descriptions;

        # identifica o tamanho do array da hierarquia
        last = len(hierarchy) - 1

        # pega somente as 50 hierarquias filhas
        # como na função findContourns foi utilizado cv.RETR_TREE, os contornos sao retornados em hierarquia
        # portanto ao pegar as ultimas x, será identificado as mais de dentro da imagem
        hierarchy = hierarchy[(last - 80):]

        arrayOfAreas = []
        arrayOfContours = []

        # pra cada contorno existente, será desenhado os que tiverem a proporção perto da placa
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            currentHierarchy = component[1]
            x,y,w,h = cv.boundingRect(currentContour)
            cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,255,0),1)

            proportion = float(w) / h

            if proportion > 2.6 and proportion < 4:
                area = cv.contourArea(currentContour)
                arrayOfAreas.append(area)
                print(frame.name + "Area: " + str(area) + "; Proportion: " + str(proportion))
                cv.rectangle(backtorgb,(x,y),(x+w,y+h),(255,255,0),1)
                arrayOfContours.append(currentContour)

            if proportion > 0.59 and proportion < 0.82:
                cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,0,255),1)
            
        areaMedia = np.mean(arrayOfAreas)

        for contour in arrayOfContours:
            areaFromContour = cv.contourArea(contour)

            if areaFromContour >= areaMedia:
                print('passou ' + frame.name + ': ' + str(areaFromContour))
                x,y,w,h = cv.boundingRect(contour)
                cv.rectangle(backtorgb,(x,y),(x+w,y+h),(255,0,0),1)
                arrayOfPlates.append(frame.originalImage[y:y+h - 5, x:x+w - 5])

        frame.arrayOfPlates = arrayOfPlates
        print('media' + frame.name + ": " + str(np.median(arrayOfAreas)))
        cv.imshow('img com contornos media' + frame.name, backtorgb)
