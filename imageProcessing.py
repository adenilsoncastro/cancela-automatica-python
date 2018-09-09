import cv2 as cv
import numpy as np
from frame import Frame
#from matplotlib import pyplot as plt
import uuid

class ImageProcessing:

    def __init__(self):
        pass

    def EqualizeHistogram(self, image):
        return cv.equalizeHist(image)
    
    def Dilate(self, image):
        kernel = np.ones((5,5), np.uint8)
        return cv.dilate(image, kernel, iterations=1)

    def GaussianBlur(self, image):
        return cv.GaussianBlur(image,(5,5),0)

    def Billateral(self, image):
        return cv.bilateralFilter(image, 8,50,50)

    def Canny(self, image):
        return cv.Canny(image, 40, 255) #145 255

    def Threshold(self, image, level):
        return cv.threshold(image, level, 255, 1)

    def ThresholdPlusOtsu(self, image, level):
        return cv.threshold(image, level, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

    def MoreLight(self, image):
        return cv.addWeighted(image,3, np.zeros(image.shape, image.dtype), 0, 20)

    def FindPossiblePlates(self, frame, usingBright, usingDilate):

        if frame.image is None:
            frame.arrayOfPlates = []
            return

        arrayOfPlates = []
        arrayOfContours = []
        arrayOfShapes = []

        # procura os contornos
        findContournsImg, contours, hierarchy = cv.findContours(frame.image.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            frame.arrayOfPlates = []
            return

        # converte a imagem pra colorida apenas para a melhor visualziação
        backtorgb = cv.cvtColor(findContournsImg, cv.COLOR_GRAY2RGB)

        hierarchy = hierarchy[-1] # get the actual inner list of hierarchy descriptions;

        # identifica o tamanho do array da hierarquia
        last = len(hierarchy) - 1

        # pega somente as 50 hierarquias filhas
        # como na função findContourns foi utilizado cv.RETR_TREE, os contornos sao retornados em hierarquia
        # portanto ao pegar as ultimas x, será identificado as mais de dentro da imagem
        hierarchy = hierarchy[(last - 100):]

        # pra cada contorno existente, será desenhado os que tiverem a proporção perto da placa
        for component in zip(contours, hierarchy):
            currentContour = component[0]
            x,y,w,h = cv.boundingRect(currentContour)
            cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,255,0),1)

            proportion = float(w) / h

            if proportion > 2.83 and proportion < 3.20:
                cv.putText(backtorgb, str(proportion), (x,y), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0),2)
                arrayOfContours.append(currentContour)

            # contorna as letras e números
            if proportion > 0.59 and proportion < 0.82:
                cv.rectangle(backtorgb,(x,y),(x+w,y+h),(0,0,255),1)

        for contour in arrayOfContours: 

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

            if height < 38:
                cv.imwrite("../rejected/height40/" + possiblePlate._id + '.png', possiblePlate.image)
                continue

            shape = height, width
            arrayOfShapes.append(shape)
            cv.drawContours(backtorgb, [contour], -1, (255,0,0), 2)
            arrayOfPlates.append(possiblePlate)

        listToRemove =[]
        i = 0
        for plate in arrayOfPlates:
            plateCopy = plate.image.copy()
            if usingBright:
                plateCopy = self.MoreLight(plateCopy)
            plateCopy = self.Billateral(plateCopy)
            plateCopy = self.Canny(plateCopy)
            if usingDilate:
                plateCopy = self.Dilate(plateCopy)
            findContournsImg, contoursPlate, hierarchy = cv.findContours(plateCopy.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            
            backtorgbplate = cv.cvtColor(plateCopy, cv.COLOR_GRAY2RGB)

            hasPlate = False

            for contour in contoursPlate:
                x,y,w,h = cv.boundingRect(contour)
                proportion = float(w) / h
                if proportion > 0.57 and proportion < 0.82 and h > 11:
                    cv.rectangle(backtorgbplate,(x,y),(x+w,y+h),(0,0,255),1)
                    hasPlate = True

            if hasPlate == False:
                listToRemove.append(plate)
                
            i = i + 1
            cv.imshow('placa ' + frame.name + " - " + str(uuid.uuid4()).split("-")[0], backtorgbplate)

        for plate in listToRemove:
            arrayOfPlates.remove(plate)
            cv.imwrite("../rejected/letter/" + frame.name + possiblePlate._id + '.png', plate.image)

        frame.arrayOfPlates = arrayOfPlates
        cv.imshow('img com contornos ' + frame.name + " - " + str(uuid.uuid4()).split("-")[0], backtorgb)
