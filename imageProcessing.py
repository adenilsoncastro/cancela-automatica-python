import cv2 as cv
import numpy as np
from frame import Frame

class ImageProcessing:

    def __init__(self):
        pass
    
    def Dilate(self, image):
        kernel = np.ones((5,5), np.uint8)
        return cv.dilate(image, kernel, iterations=1)

    def GaussianBlur(self, image):
        return cv.GaussianBlur(image,(5,5),0)

    def Billateral(self, image):
        return cv.bilateralFilter(image, 8,50,50)

    def Canny(self, image):
        return cv.Canny(image, 145, 255)

    def Threshold(self, image, level):
        return cv.threshold(image, level, 255, 1)

    def FindPossiblePlates(self, frame):

        # cv.imshow('inicial ' + frame.name, frame.image)
        arrayOfPlates = []
        arrayOfAreas = []
        arrayOfContours = []
        arrayOfShapes = []

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

        # pra cada contorno existente, será desenhado os que tiverem a proporção perto da placa
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            currentHierarchy = component[1]
            x,y,w,h = cv.boundingRect(currentContour)
            cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,255,0),1)

            proportion = float(w) / h

            if proportion > 2.83 and proportion < 3.20:
                area = cv.contourArea(currentContour)
                arrayOfAreas.append(area)
                #print(frame.name + " Area: " + str(area) + "; Proportion: " + str(proportion))
                cv.putText(backtorgb, str(proportion), (x,y), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),2)
                arrayOfContours.append(currentContour)

            # contorna as letras e números
            # if proportion > 0.59 and proportion < 0.82:
            #     cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,0,255),1)
            
        areaMedia = np.mean(arrayOfAreas)
        #print('media ' + frame.name + ": " + str(areaMedia))

        for contour in arrayOfContours:
            areaFromContour = cv.contourArea(contour)

            if areaFromContour >= areaMedia:
                x,y,w,h = cv.boundingRect(contour)

                possiblePlate = Frame(frame.originalImage[y:y+h, x:x+w], frame.name, None, None)        
                height, width = possiblePlate.image.shape

                # remove placas duplicadas
                plateAlreadyExists = False
                for shape in arrayOfShapes:
                    if(shape[0] == height and shape[1] == width):
                        plateAlreadyExists = True

                if plateAlreadyExists:
                    continue

                calculatedArea = height * width
                shape = height, width
                arrayOfShapes.append(shape)

                if calculatedArea > 760:
                    #print('passou ' + frame.name + ': ' + str(areaFromContour))
                    #print('height: ' + str(height) + '; width: ' + str(width))
                
                    # cv.rectangle(backtorgb,(x,y),(x+w,y+h),(255,0,0),1)
                    cv.drawContours(backtorgb, [contour], -1, (255,0,0), 2)
                    arrayOfPlates.append(possiblePlate)
                
            
        frame.arrayOfPlates = arrayOfPlates
        cv.imshow('img com contornos media' + frame.name, backtorgb)

